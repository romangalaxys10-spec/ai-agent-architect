"""
SAST Sentinel Engine.
OWASP Top-10 aligned static security analysis with severity, exploitability,
remediation snippets, and a CI-gate compliance verdict.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class VulnFinding:
    rule: str
    owasp: str
    severity: str
    cvss_like: float
    line: int
    evidence: str
    remediation: str
    exploit_path: str

@dataclass
class ScanReport:
    language_guess: str
    findings: List[VulnFinding] = field(default_factory=list)
    secure_default_hits: List[str] = field(default_factory=list)
    verdict: str = ""
    risk_score: float = 0.0

CHECKS = [
    dict(rule="SQL_INJECTION", owasp="A03:2021 Injection", severity="critical", cvss=9.1,
         pattern=r"(execute|executemany|cursor\.\w+)\s*\(\s*f?([\"'])\s*(SELECT|INSERT|UPDATE|DELETE|DROP)[^\"']*(\+|%|\{)[^\"']*\2",
         remediation="cursor.execute('SELECT ... WHERE id = %s', (user_id,))",
         exploit="Attacker closes the string, appends UNION SELECT, exfiltrates adjacent tables."),
    dict(rule="XSS_REFLECTED", owasp="A03:2021 Injection", severity="high", cvss=7.4,
         pattern=r"(innerHTML|document\.write|\|\s*safe\b)\s*[=(].{0,60}(request\.|params\.|input|req\.)",
         remediation="Escape on output (html.escape) + Content-Security-Policy; never mark user HTML as safe.",
         exploit="Script tag in a query param executes in every visitor's session."),
    dict(rule="HARDCODED_SECRET", owasp="A07:2021 Identification & Auth Failures", severity="critical", cvss=9.0,
         pattern=r"(?i)(api[_-]?key|secret|password|passwd|token|private[_-]?key)\s*[:=]\s*[\"'][A-Za-z0-9_\-+/=]{12,}[\"']",
         remediation="os.environ['SECRET_NAME'] + rotate the committed value now (it is burned).",
         exploit="Repo scrape bots find the literal within minutes; full API takeover."),
    dict(rule="DESERIALIZATION_RCE", owasp="A08:2021 Software & Data Integrity", severity="critical", cvss=9.8,
         pattern=r"(pickle\.load|yaml\.load\s*\((?![^)]*Loader\s*=\s*yaml\.SafeLoader)|marshal\.load)",
         remediation="json.loads(...) or yaml.safe_load(...); validate against a schema.",
         exploit="Crafted pickle executes arbitrary __reduce__ payloads on load."),
    dict(rule="PATH_TRAVERSAL", owasp="A01:2021 Broken Access Control", severity="high", cvss=7.5,
         pattern=r"open\s*\(\s*(request\.|os\.path\.join\([^)]*(req|param|user))",
         remediation="Resolve then verify: p = Path(base, user_path).resolve(); assert str(p).startswith(str(BASE)).",
         exploit="../../../../etc/passwd read/write outside the sandbox."),
    dict(rule="COMMAND_INJECTION", owasp="A03:2021 Injection", severity="critical", cvss=9.5,
         pattern=r"(os\.system|subprocess\.\w+|os\.popen)\s*\([^)]*(\+|%|f[\"']|\{)\s*(req|param|user|input)",
         remediation="subprocess.run([bin, *validated_args], shell=False) with an allowlist.",
         exploit="Semicolon in the parameter chains a second command."),
    dict(rule="WEAK_CRYPTO", owasp="A02:2021 Cryptographic Failures", severity="high", cvss=7.4,
         pattern=r"(hashlib\.(md5|sha1)\s*\(|DES\b|ECB\b|random\.\w+\(\).{0,30}(token|key|secret))",
         remediation="hashlib.sha256/sha512; secrets.token_hex(32); AES-GCM via a vetted library.",
         exploit="Offline brute-force of weak hashes; predictable tokens are guessable."),
    dict(rule="TLS_BYPASS", owasp="A02:2021 Cryptographic Failures", severity="high", cvss=7.4,
         pattern=r"(verify\s*=\s*False|CERT_NONE|check_hostname\s*=\s*False|sslv3|tlsv1[^\.])",
         remediation="verify=True with a pinned CA bundle where needed.",
         exploit="MITM on the same network reads and rewrites the 'encrypted' traffic."),
    dict(rule="DEBUG_IN_PROD", owasp="A05:2021 Security Misconfiguration", severity="medium", cvss=5.3,
         pattern=r"(debug\s*=\s*True|FLASK_ENV\s*=\s*['\"]development)",
         remediation="drive debug from an env flag defaulting to False; add a config test.",
         exploit="Interactive traceback console gives RCE on error pages."),
    dict(rule="JWT_WEAK", owasp="A07:2021 Identification & Auth Failures", severity="high", cvss=8.1,
         pattern=r"(algorithm[s]?\s*[=:]\s*[\[\]\"']\s*(none|HS256)[\"']?).{0,80}(algorithms?\s*[=:]\s*[\[\]\"']none)",
         remediation="jwt.decode(token, key, algorithms=['RS256']) with issuer/audience checks.",
         exploit="alg=none forgery mints admin tokens."),
    dict(rule="OPEN_REDIRECT", owasp="A01:2021 Broken Access Control", severity="medium", cvss=6.1,
         pattern=r"(redirect|RedirectResponse|HttpResponseRedirect)\s*\(\s*(request\.(GET|args|args\.get)|params)",
         remediation="Validate against an allowlist of exact target hosts before redirecting.",
         exploit="Phishing links ride your trusted domain to attacker sites."),
    dict(rule="LOG_INJECTION", owasp="A09:2021 Logging & Monitoring Failures", severity="low", cvss=3.7,
         pattern=r"(logging\.\w+|logger\.\w+)\s*\(\s*(f?[\"'][^\"']*\{?)(request\.|user_input|req\.)",
         remediation="Strip newlines/control chars before logging untrusted strings.",
         exploit="Forged log lines fake audit trails and poison log parsers."),
]

SECURE_DEFAULTS = [
    (r"verify\s*=\s*True", "TLS verification explicit"),
    (r"safe_load", "yaml safe loader"),
    (r"parameterized|executescript\(\s*\?", "parameterized SQL"),
    (r"secrets\.", "secrets module"),
    (r"html\.escape", "output escaping"),
    (r"algorithms\s*=\s*[\[\]\"']RS256", "asymmetric JWT"),
]

class SASTSentinelEngine:
    """Assume breach: every sink is guilty until the pattern proves guarded."""

    @classmethod
    def scan(cls, code: str) -> ScanReport:
        lang = ("python" if re.search(r"\b(def |import |self\.)", code)
                else "javascript" if re.search(r"\b(function|const |require\()", code)
                else "generic")
        findings: List[VulnFinding] = []
        for idx, line in enumerate(code.splitlines(), 1):
            if line.strip().startswith(("#", "//", "*")):
                continue
            for chk in CHECKS:
                if re.search(chk["pattern"], line, re.I):
                    findings.append(VulnFinding(
                        rule=chk["rule"], owasp=chk["owasp"], severity=chk["severity"],
                        cvss_like=chk["cvss"], line=idx, evidence=line.strip()[:100],
                        remediation=chk["remediation"], exploit_path=chk["exploit"]))

        secure = [label for pat, label in SECURE_DEFAULTS if re.search(pat, code)]
        sev_mult = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        risk = round(sum(sev_mult[f.severity] for f in findings) * 2.5, 1)
        crit = [f for f in findings if f.severity == "critical"]
        high = [f for f in findings if f.severity == "high"]
        verdict = ("FAIL_SECURITY_GATE" if crit or len(high) >= 3
                   else "PASS_WITH_WARNINGS" if findings else "PASS")
        return ScanReport(language_guess=lang, findings=findings,
                          secure_default_hits=secure, verdict=verdict, risk_score=risk)

    @staticmethod
    def format_report(r: ScanReport) -> str:
        out = ["=" * 62, "SAST SENTINEL AGENT — SECURITY SCAN", "=" * 62,
               f"Language: {r.language_guess} | risk score: {r.risk_score} | verdict: {r.verdict}",
               f"Findings: {len(r.findings)} " + (
                   f"({len([f for f in r.findings if f.severity=='critical'])} critical / "
                   f"{len([f for f in r.findings if f.severity=='high'])} high)" if r.findings else ""),
               "-" * 62]
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        for f in sorted(r.findings, key=lambda f: order[f.severity]):
            out.append(f"[{f.severity.upper():8}] L{f.line:<4} {f.rule} ({f.owasp}) cvss~{f.cvss_like}")
            out.append(f"    evidence: {f.evidence}")
            out.append(f"    exploit : {f.exploit_path}")
            out.append(f"    fix     : {f.remediation}")
        if not r.findings:
            out.append("No vulnerable patterns matched.")
        if r.secure_default_hits:
            out += ["-" * 62, "Secure defaults detected: " + ", ".join(r.secure_default_hits)]
        out += ["=" * 62,
                "Note: pattern-based SAST — pair with a secrets scanner and dependency audit in CI."]
        return "\n".join(out)
