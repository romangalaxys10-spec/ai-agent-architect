"""
SysAdmin demo — smoke through 90-series agents offline.
Run: python examples/sysadmin_demo.py
"""
import importlib.util, os, sys
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)
samples=[
    ("solana-validator-ops-agent","solana_validator_ops","Solana validator vote account snapshot sync with delinquency triage and enough words to pass check"),
    ("evm-node-ops-agent","evm_node_ops","EVM node Geth Erigon sync peering pruning for blockchain ops with enough words"),
    ("linux-boot-rescue-agent","linux_boot_rescue","Linux boot rescue GRUB initramfs rescue mode forensics with enough words"),
    ("vuln-triage-agent","vuln_triage","Vuln triage CVE EPSS patch priority with enough words"),
    ("deep-debugger-agent","deep_debugger","Deep debugger bisect time travel trace stitching with enough words"),
    ("llm-local-deployer-agent","llm_local_deployer","LLM local deploy Ollama vLLM GGUF with VRAM and TTFT with enough words"),
    ("figma-to-code-agent","figma_to_code","Figma to code autolayout Tailwind token fidelity with enough words"),
    ("frontend-scaffold-agent","frontend_scaffold","Frontend scaffold Vite Next.js with TS lint and a11y baseline with enough words"),
]
for slug, module, text in samples:
    path=os.path.join(REPO,"agents",slug,"core",f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(slug.replace("-","_"), path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Engine=[v for v in mod.__dict__.values() if hasattr(v,"analyze")][0]
    result=Engine.analyze(text)
    print(Engine.format_report(result))
    print("\n"+"="*80+"\n")
