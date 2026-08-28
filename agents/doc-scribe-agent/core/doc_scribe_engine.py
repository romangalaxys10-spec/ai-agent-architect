"""
Doc Scribe Engine.
Reverse-engineers documentation from Python source: API reference tables,
usage examples, and undocumented-symbol flags.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class APISymbol:
    name: str
    kind: str
    signature: str
    docstring: bool
    params: List[str] = field(default_factory=list)
    example: str = ""

@dataclass
class DocPack:
    module_summary: str
    symbols: List[APISymbol] = field(default_factory=list)
    undocumented_public: List[str] = field(default_factory=list)
    doc_md: str = ""
    stale_hints: List[str] = field(default_factory=list)
    verdict: str = ""

class DocScribeEngine:
    """Documentation that cannot drift silently: gaps are surfaced, not hidden."""

    @classmethod
    def document(cls, source: str, style: str = "markdown") -> DocPack:
        lines = source.splitlines()
        symbols: List[APISymbol] = []
        i = 0
        module_doc = ""
        if lines and (lines[0].startswith('"""') or lines[0].startswith("'''")):
            quote = lines[0][:3]
            if lines[0].count(quote) >= 2 and len(lines[0]) > 6:
                module_doc = lines[0][3:-3]
            else:
                buf = [lines[0][3:]]
                i = 1
                while i < len(lines) and quote not in lines[i]:
                    buf.append(lines[i]); i += 1
                module_doc = " ".join(b.strip() for b in buf if b.strip())[:200]

        sig_re = re.compile(r"^\s*(def|class)\s+(\w+)\s*(\(([^)]*)\))?")
        while i < len(lines):
            m = sig_re.match(lines[i])
            if m:
                kind, name, _, argstr = m.group(1), m.group(2), m.group(3), m.group(4) or ""
                # collect docstring presence
                has_doc = False
                for j in range(i + 1, min(i + 4, len(lines))):
                    if lines[j].strip().startswith(('"""', "'''")):
                        has_doc = True
                        break
                    if lines[j].strip() and not lines[j].strip().startswith((")", "#", "@")):
                        break
                params = [a.split(":")[0].split("=")[0].strip()
                          for a in argstr.split(",") if a.strip()]
                params = [p for p in params if p not in ("self", "cls")]
                sig = f"{name}({', '.join(params)})"
                arg_preview = ", ".join(params[:2]) if params else ""
                example = (f"{name}({arg_preview})" if kind == "def"
                           else f"{name}()")
                symbols.append(APISymbol(name, kind, sig, has_doc, params, example))
            i += 1

        public = [s for s in symbols if not s.name.startswith("_")]
        undocumented = [s.name for s in public if not s.docstring]
        all_names = {s.name for s in symbols}

        # stale-doc hints: docstring mentions names that no longer exist
        doc_blob = " ".join(re.findall(r'"""(.*?)"""', source, re.S))
        for word in set(re.findall(r"\b[A-Za-z_]\w{4,}\b", doc_blob)):
            if word not in all_names and word[:1].islower() and word in doc_blob and \
               re.search(rf"\b{word}\b", doc_blob) and word not in ("returns", "param", "type", "example"):
                cls._stale.append(word)
        stale = sorted(set(cls._stale))[:5]
        cls._stale = []

        md = [f"# Module API Reference", ""]
        if module_doc:
            md += [f"> {module_doc}", ""]
        md += ["## Public API", ""]
        if not public:
            md += ["*(no public callables found)*", ""]
        for s in public:
            md.append(f"### `{s.signature}`" + ("" if s.kind == "def" else " *(class)*"))
            md.append("")
            if s.params:
                md.append("| Parameter | Type hint | Description |")
                md.append("|---|---|---|")
                for p in s.params:
                    md.append(f"| `{p}` | *(fill in)* | *(fill in)* |")
                md.append("")
            md.append("```python")
            md.append(f"{s.example}  # TODO: real example")
            md.append("```")
            md.append("")
        md += ["## Private API (internal)", ""]
        priv = [s for s in symbols if s.name.startswith("_") and s.name not in ("__init__",)]
        md += [f"- `{s.signature}`" for s in priv] or ["*(none)*"]

        doc_pct = round(100 * len([s for s in public if s.docstring]) / len(public), 0) if public else 100.0
        verdict = f"DOC_COVERAGE {doc_pct:.0f}% | {len(undocumented)} undocumented public symbols"
        return DocPack(module_summary=module_doc or "(no module docstring)",
                       symbols=symbols, undocumented_public=undocumented,
                       doc_md="\n".join(md), stale_hints=stale, verdict=verdict)

    _stale: list = []

    @staticmethod
    def format_docs(pack: DocPack) -> str:
        out = ["=" * 62, "DOC SCRIBE AGENT — DOCUMENTATION PACK", "=" * 62, pack.verdict, "-" * 62]
        if pack.undocumented_public:
            out.append("Undocumented public symbols (fix first):")
            out += [f"  - {n}" for n in pack.undocumented_public]
        else:
            out.append("All public symbols documented.")
        if pack.stale_hints:
            out.append("Possible stale references in docstrings: "
                       + ", ".join(pack.stale_hints))
        out += ["-" * 62, "Generated reference:", ""]
        out += pack.doc_md.splitlines()
        out += ["", "=" * 62]
        return "\n".join(out)
