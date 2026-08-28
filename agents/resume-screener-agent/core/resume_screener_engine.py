"""
Resume Screener Agent Engine.
Scores resume-job fit with per-skill evidence, estimates experience,
flags red flags, and enforces bias-safe language in the output itself.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class SkillMatch:
    skill: str
    required: bool
    matched: bool
    evidence: str

@dataclass
class ScreenResult:
    fit_score: float
    skills: List[SkillMatch] = field(default_factory=list)
    years_estimate: float = 0.0
    red_flags: List[str] = field(default_factory=list)
    interview_probes: List[str] = field(default_factory=list)
    bias_audit: List[str] = field(default_factory=list)
    recommendation: str = ""
    verdict: str = ""

SKILL_ALIASES = {
    "python": ["python", "django", "flask", "fastapi", "pandas", "numpy"],
    "javascript": ["javascript", "js", "react", "vue", "node", "typescript"],
    "typescript": ["typescript", "ts", "react", "node"],
    "go": ["golang", "go "],
    "rust": ["rust"],
    "sql": ["sql", "postgres", "mysql", "sqlite", "bigquery"],
    "aws": ["aws", "ec2", "s3", "lambda", "cloudformation"],
    "kubernetes": ["kubernetes", "k8s", "helm", "eks"],
    "docker": ["docker", "container", "podman"],
    "ml": ["machine learning", "ml ", "pytorch", "tensorflow", "sklearn", "scikit", "llm", "deep learning"],
    "leadership": ["led", "managed", "mentored", "team lead", "head of", "supervised"],
    "system_design": ["system design", "architecture", "distributed", "scalab", "microservice"],
}

BIAS_TERMS = {
    "rockstar": "uses 'rockstar' — gendered/culture-loaded; use 'high-performing'",
    "ninja": "uses 'ninja' — culture-loaded; name the actual skill",
    "young": "references youth — age-protected; drop it",
    "energetic": "'energetic' is an age proxy — describe the work instead",
    "native speaker": "'native speaker' is national-origin proxy — say 'professional proficiency'",
    "culture fit": "'culture fit' is a bias launderer — use 'values alignment' with named values",
    "recent grad": "'recent grad' excludes older career-changers — use 'early-career'",
}

class ResumeScreenerEngine:
    """Score the evidence, not the pedigree — and clean your own bias first."""

    @classmethod
    def screen(cls, resume_text: str, job_text: str) -> ScreenResult:
        res_low, job_low = resume_text.lower(), job_text.lower()

        # extract required skills from job text
        required = []
        for m in re.finditer(r"(?:requires?|must have|proficien\w+ in|strong|expert(?:ise)? in|experience with)\s+"
                             r"([a-z][a-z+#.\s]{2,40})", job_low):
            for piece in re.split(r"\s*(?:,|and|/|;)\s*", m.group(1).strip()):
                piece = piece.strip(" .")
                if 2 < len(piece) < 25 and piece not in required and not piece.isdigit():
                    required.append(piece)
        for skill in SKILL_ALIASES:
            if any(alias in job_low for alias in SKILL_ALIASES[skill]):
                if skill not in required:
                    required.append(skill)
        required = required[:12]
        if not required:
            required = ["python", "sql", "system_design"]

        nice = []
        for m in re.finditer(r"(?:nice to have|bonus|preferred|plus)\s*[:\-]?\s*([a-z][a-z+#.\s]{2,40})", job_low):
            for piece in re.split(r"\s*(?:,|and|/|;)\s*", m.group(1).strip()):
                if 2 < len(piece) < 25 and piece not in required and piece not in nice:
                    nice.append(piece)
        nice = nice[:6]

        # match skills with evidence snippets
        skills = []
        matched_req = 0
        for skill in required:
            aliases = SKILL_ALIASES.get(skill, [skill])
            hit = None
            for alias in aliases:
                idx = res_low.find(alias if alias.endswith(" ") else alias)
                if idx >= 0:
                    start = max(0, idx - 30)
                    hit = resume_text[start:idx + len(alias) + 40].replace("\n", " ").strip()
                    break
            ok = hit is not None
            matched_req += 1 if ok else 0
            skills.append(SkillMatch(skill, True, ok, (f"...{hit[:80]}..." if ok else "NOT FOUND in resume")))
        matched_nice = 0
        for skill in nice:
            if skill in res_low or any(a in res_low for a in SKILL_ALIASES.get(skill, [skill])):
                matched_nice += 1
                skills.append(SkillMatch(skill, False, True, "present"))
            else:
                skills.append(SkillMatch(skill, False, False, "not present (nice-to-have)"))

        # years of experience estimate
        years = 0.0
        ym = re.findall(r"(\d{1,2})\+?\s*(?:years?|yrs?)", res_low)
        if ym:
            years = max(float(y) for y in ym if float(y) < 45)
        else:
            # count distinct role ranges as a rough proxy
            ranges = re.findall(r"(20\d{2})\s*[-–to]+\s*(20\d{2}|present|current)", res_low, re.I)
            for start, end in ranges:
                end_y = 2026 if end.lower() in ("present", "current") else int(end)
                years += max(0, end_y - int(start))
            years = min(years, 40)

        req_years = 0.0
        jym = re.search(r"(\d{1,2})\+?\s*(?:years?|yrs?)", job_low)
        if jym:
            req_years = float(jym.group(1))

        red_flags = []
        if req_years and years + 1 < req_years:
            red_flags.append(f"Experience gap: resume reads ~{years:.0f}y vs required {req_years:.0f}y — "
                             f"verify depth in screening call.")
        # job hopping: many short stints
        ranges = re.findall(r"(20\d{2})\s*[-–to]+\s*(20\d{2}|present|current)", res_low, re.I)
        short = 0
        for start, end in ranges:
            end_y = 2026 if end.lower() in ("present", "current") else int(end)
            if 0 < end_y - int(start) < 1 and (end_y - int(start)) >= 0:
                short += 1
        if len(ranges) >= 4 and short >= 2:
            red_flags.append(f"{short} sub-year stints among {len(ranges)} roles — ask about context, don't assume.")
        if not re.search(r"\b(led|owned|shipped|delivered|built|drove|launched)\b", res_low):
            red_flags.append("No ownership verbs — contribution level is unclear (pair with structured interview).")

        # fit score
        req_cover = matched_req / max(1, len([s for s in skills if s.required]))
        nice_cover = matched_nice / max(1, len(nice)) if nice else 0.5
        years_ok = 1.0 if (not req_years or years >= req_years - 1) else 0.5
        fit = round(100 * (0.55 * req_cover + 0.15 * nice_cover + 0.30 * years_ok), 1)

        probes = []
        for s in skills:
            if s.required and not s.matched:
                probes.append(f"Probe '{s.skill}': ask for the closest adjacent experience and a concrete artifact.")
        if red_flags:
            probes.append("Probe tenure: 'walk me through why each move happened' — listen for judgment, not loyalty.")
        if not probes:
            probes.append("All requirements evidenced — probe DEPTH: 'tell me about the hardest failure with this skill.'")

        # bias audit on BOTH documents
        bias = []
        for term, fix in BIAS_TERMS.items():
            if term in job_low:
                bias.append(f"JOB DESC {fix}.")
            if term in res_low:
                bias.append(f"RESUME {fix} — ignore this signal when scoring.")
        if re.search(r"\b(gpa|university ranking|ivy|prestigious)\b", job_low):
            bias.append("JOB DESC signals pedigree weighting — skills evidence is the defensible criterion.")
        if not bias:
            bias.append("No bias-pattern language detected in either document.")

        if fit >= 75:
            rec = "ADVANCE to technical screen — evidence covers requirements."
        elif fit >= 55:
            rec = "SCREENING CALL first — verify the gaps are real, not resume-phrasing artifacts."
        else:
            rec = "DO NOT ADVANCE on current evidence — send a skills-specific follow-up or reject honestly."

        verdict = f"FIT {fit:.0f}/100 | required skills {matched_req}/{len([s for s in skills if s.required])} | ~{years:.0f}y experience"
        return ScreenResult(fit, skills, years, red_flags, probes, bias, rec, verdict)

    @staticmethod
    def format_result(r: ScreenResult) -> str:
        out = ["=" * 62, "RESUME SCREENER AGENT — RESULT", "=" * 62, r.verdict, "-" * 62,
               "Skill evidence:"]
        for s in r.skills:
            mark = "PASS" if s.matched else ("MISS" if s.required else "----")
            out.append(f"  [{mark}] {s.skill[:18]:18} {'(required)' if s.required else '(nice)'}")
            out.append(f"         {s.evidence[:88]}")
        out += [f"-" * 62, f"Experience estimate: ~{r.years_estimate:.0f} years (verify verbally)"]
        if r.red_flags:
            out += ["Red flags (context needed, not verdicts):"] + [f"  ! {x}" for x in r.red_flags]
        out += ["-" * 62, "Interview probes:"]
        out += [f"  ? {p}" for p in r.interview_probes]
        out += ["-" * 62, "Bias audit (language hygiene):"]
        out += [f"  * {b}" for b in r.bias_audit]
        out += ["-" * 62, f"RECOMMENDATION: {r.recommendation}",
                "=" * 62,
                "Compliance note: score job-related evidence only; document the reason for every advance/reject."]
        return "\n".join(out)
