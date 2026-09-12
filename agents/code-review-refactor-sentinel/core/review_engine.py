"""
Code Review & Refactoring Sentinel Engine.
AST-based static analysis, security vulnerability scanning, anti-pattern detection, and patch generation.
"""

import ast
import re
import difflib
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class CodeIssue:
    line_number: int
    rule_id: str
    severity: str
    message: str
    suggested_fix: str


@dataclass
class ReviewReport:
    file_path: str
    total_lines: int
    complexity_score: int
    issues: List[CodeIssue]
    refactored_code: Optional[str] = None
    diff_patch: Optional[str] = None
    verdict: str = "PASS"


class CodeReviewEngine:
    """Performs deep AST security and code quality audits."""

    @classmethod
    def analyze_code(cls, source_code: str, file_path: str = "source.py") -> ReviewReport:
        issues: List[CodeIssue] = []
        lines = source_code.splitlines()
        total_lines = len(lines)

        for idx, line in enumerate(lines, 1):
            if re.search(r'(?i)(api_key|api-key|secret|token|password)\s*=\s*["\'][A-Za-z0-9_\-]{16,}["\']', line):
                issues.append(CodeIssue(
                    line_number=idx,
                    rule_id="SEC-001",
                    severity="CRITICAL",
                    message="Hardcoded API key or credential detected.",
                    suggested_fix="Externalize into environment variables."
                ))
            if re.search(r'eval\s*\(|exec\s*\(', line):
                issues.append(CodeIssue(
                    line_number=idx,
                    rule_id="SEC-002",
                    severity="CRITICAL",
                    message="Dangerous eval() or exec() usage allows arbitrary code execution.",
                    suggested_fix="Use safe AST-based literals or predefined mappings."
                ))
            if re.search(r'subprocess\.(Popen|run|call)\(.*shell\s*=\s*True', line):
                issues.append(CodeIssue(
                    line_number=idx,
                    rule_id="SEC-003",
                    severity="HIGH",
                    message="Subprocess execution with shell=True invites command injection.",
                    suggested_fix="Pass arguments as a list with shell=False."
                ))

        complexity = 1
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With)):
                    complexity += 1
                
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    issues.append(CodeIssue(
                        line_number=node.lineno,
                        rule_id="QUAL-001",
                        severity="MEDIUM",
                        message="Bare 'except:' clause catches SystemExit and KeyboardInterrupt.",
                        suggested_fix="Catch specific exceptions like 'except Exception:'."
                    ))

                if isinstance(node, ast.FunctionDef):
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            issues.append(CodeIssue(
                                line_number=node.lineno,
                                rule_id="QUAL-002",
                                severity="HIGH",
                                message="Mutable default argument in function: " + node.name,
                                suggested_fix="Use None as default and initialize inside body."
                            ))
        except SyntaxError as e:
            issues.append(CodeIssue(
                line_number=e.lineno or 1,
                rule_id="SYNTAX-ERR",
                severity="CRITICAL",
                message="Syntax error in code: " + str(e.msg),
                suggested_fix="Fix syntax error."
            ))

        refactored = source_code
        refactored = re.sub(r'except\s*:\s*\n', 'except Exception:\n', refactored)
        
        diff = ""
        if refactored != source_code:
            diff_lines = difflib.unified_diff(
                source_code.splitlines(keepends=True),
                refactored.splitlines(keepends=True),
                fromfile="a/" + file_path,
                tofile="b/" + file_path
            )
            diff = "".join(diff_lines)

        critical_count = sum(1 for i in issues if i.severity in ("CRITICAL", "HIGH"))
        verdict = "FAIL" if critical_count > 0 else ("WARN" if issues else "PASS")

        return ReviewReport(
            file_path=file_path,
            total_lines=total_lines,
            complexity_score=complexity,
            issues=issues,
            refactored_code=refactored if diff else None,
            diff_patch=diff if diff else None,
            verdict=verdict
        )
