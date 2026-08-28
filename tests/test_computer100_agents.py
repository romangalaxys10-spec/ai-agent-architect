"""Contract + functional tests for the 100 Computer Use series.

Every agent: OS-aware offline engine + CLI (--os) + SKILL.md contract.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AGENTS_DIR = os.path.join(REPO_ROOT, "agents")

COMPUTER100 = [
    ("computer-vision-agent", "computer_vision", "ComputerVisionEngine"),
    ("desktop-automation-agent", "desktop_automation", "DesktopAutomationEngine"),
    ("screen-recorder-agent", "screen_recorder", "ScreenRecorderEngine"),
    ("accessibility-pilot-agent", "accessibility_pilot", "AccessibilityPilotEngine"),
    ("keyboard-maestro-agent", "keyboard_maestro", "KeyboardMaestroEngine"),
    ("mouse-precision-agent", "mouse_precision", "MousePrecisionEngine"),
    ("clipboard-ops-agent", "clipboard_ops", "ClipboardOpsEngine"),
    ("file-explorer-agent", "file_explorer", "FileExplorerEngine"),
    ("notification-center-agent", "notification_center", "NotificationCenterEngine"),
    ("system-prefs-agent", "system_prefs", "SystemPrefsEngine"),
    ("spotlight-search-agent", "spotlight_search", "SpotlightSearchEngine"),
    ("window-tiling-agent", "window_tiling", "WindowTilingEngine"),
    ("menubar-tray-agent", "menubar_tray", "MenubarTrayEngine"),
    ("screenshot-assert-agent", "screenshot_assert", "ScreenshotAssertEngine"),
    ("drag-drop-orchestrator-agent", "drag_drop_orchestrator", "DragDropOrchestratorEngine"),
    ("touch-gesture-agent", "touch_gesture", "TouchGestureEngine"),
    ("ocr-reader-agent", "ocr_reader", "OcrReaderEngine"),
    ("audio-router-agent", "audio_router", "AudioRouterEngine"),
    ("camera-mic-governor-agent", "camera_mic_governor", "CameraMicGovernorEngine"),
    ("power-battery-agent", "power_battery", "PowerBatteryEngine"),
    ("display-color-agent", "display_color", "DisplayColorEngine"),
    ("input-device-agent", "input_device", "InputDeviceEngine"),
    ("browser-pilot-agent", "browser_pilot", "BrowserPilotEngine"),
    ("cdp-bridge-agent", "cdp_bridge", "CdpBridgeEngine"),
    ("playwright-orchestrator-agent", "playwright_orchestrator", "PlaywrightOrchestratorEngine"),
    ("puppeteer-forge-agent", "puppeteer_forge", "PuppeteerForgeEngine"),
    ("selenium-grid-agent", "selenium_grid", "SeleniumGridEngine"),
    ("browser-extension-agent", "browser_extension", "BrowserExtensionEngine"),
    ("dom-forensics-agent", "dom_forensics", "DomForensicsEngine"),
    ("web-scraper-agent", "web_scraper", "WebScraperEngine"),
    ("form-autofill-agent", "form_autofill", "FormAutofillEngine"),
    ("cookie-consent-agent", "cookie_consent", "CookieConsentEngine"),
    ("storage-inspector-agent", "storage_inspector", "StorageInspectorEngine"),
    ("network-har-agent", "network_har", "NetworkHarEngine"),
    ("performance-audit-agent", "performance_audit", "PerformanceAuditEngine"),
    ("accessibility-web-agent", "accessibility_web", "AccessibilityWebEngine"),
    ("visual-regression-agent", "visual_regression", "VisualRegressionEngine"),
    ("auth-session-agent", "auth_session", "AuthSessionEngine"),
    ("download-manager-agent", "download_manager", "DownloadManagerEngine"),
    ("pdf-renderer-agent", "pdf_renderer", "PdfRendererEngine"),
    ("webrtc-media-agent", "webrtc_media", "WebrtcMediaEngine"),
    ("service-worker-agent", "service_worker", "ServiceWorkerEngine"),
    ("web-security-agent", "web_security", "WebSecurityEngine"),
    ("browser-profile-agent", "browser_profile", "BrowserProfileEngine"),
    ("shell-pilot-agent", "shell_pilot", "ShellPilotEngine"),
    ("pty-bridge-agent", "pty_bridge", "PtyBridgeEngine"),
    ("tmux-orchestrator-agent", "tmux_orchestrator", "TmuxOrchestratorEngine"),
    ("terminal-renderer-agent", "terminal_renderer", "TerminalRendererEngine"),
    ("cli-scaffold-agent", "cli_scaffold", "CliScaffoldEngine"),
    ("prompt-engineer-agent", "prompt_engineer", "PromptEngineerEngine"),
    ("history-forensics-agent", "history_forensics", "HistoryForensicsEngine"),
    ("autocomplete-intel-agent", "autocomplete_intel", "AutocompleteIntelEngine"),
    ("env-shell-agent", "env_shell", "EnvShellEngine"),
    ("ssh-remote-agent", "ssh_remote", "SshRemoteEngine"),
    ("terminal-recorder-agent", "terminal_recorder", "TerminalRecorderEngine"),
    ("log-tail-agent", "log_tail", "LogTailEngine"),
    ("job-control-agent", "job_control", "JobControlEngine"),
    ("keybinding-doctor-agent", "keybinding_doctor", "KeybindingDoctorEngine"),
    ("terminal-security-agent", "terminal_security", "TerminalSecurityEngine"),
    ("repl-bridge-agent", "repl_bridge", "ReplBridgeEngine"),
    ("man-help-agent", "man_help", "ManHelpEngine"),
    ("shell-benchmark-agent", "shell_benchmark", "ShellBenchmarkEngine"),
    ("linux-admin-agent", "linux_admin", "LinuxAdminEngine"),
    ("systemd-surgeon-agent", "systemd_surgeon", "SystemdSurgeonEngine"),
    ("package-manager-agent", "package_manager", "PackageManagerEngine"),
    ("kernel-tuner-agent", "kernel_tuner", "KernelTunerEngine"),
    ("network-ops-agent", "network_ops", "NetworkOpsEngine"),
    ("storage-raid-agent", "storage_raid", "StorageRaidEngine"),
    ("log-rotation-agent", "log_rotation", "LogRotationEngine"),
    ("backup-restore-agent", "backup_restore", "BackupRestoreEngine"),
    ("sec-hardening-agent", "sec_hardening", "SecHardeningEngine"),
    ("container-ops-agent", "container_ops", "ContainerOpsEngine"),
    ("k8s-pilot-agent", "k8s_pilot", "K8sPilotEngine"),
    ("nginx-ops-agent", "nginx_ops", "NginxOpsEngine"),
    ("macos-admin-agent", "macos_admin", "MacosAdminEngine"),
    ("brew-ops-agent", "brew_ops", "BrewOpsEngine"),
    ("xcode-ops-agent", "xcode_ops", "XcodeOpsEngine"),
    ("macos-security-agent", "macos_security", "MacosSecurityEngine"),
    ("windows-admin-agent", "windows_admin", "WindowsAdminEngine"),
    ("powershell-forge-agent", "powershell_forge", "PowershellForgeEngine"),
    ("winget-choco-agent", "winget_choco", "WingetChocoEngine"),
    ("windows-security-agent", "windows_security", "WindowsSecurityEngine"),
    ("ad-identity-agent", "ad_identity", "AdIdentityEngine"),
    ("ci-cd-orchestrator-agent", "ci_cd_orchestrator", "CiCdOrchestratorEngine"),
    ("observability-stack-agent", "observability_stack", "ObservabilityStackEngine"),
    ("infra-provisioner-agent", "infra_provisioner", "InfraProvisionerEngine"),
    ("ansible-pilot-agent", "ansible_pilot", "AnsiblePilotEngine"),
    ("tls-cert-agent", "tls_cert", "TlsCertEngine"),
    ("db-ops-agent", "db_ops", "DbOpsEngine"),
    ("queue-ops-agent", "queue_ops", "QueueOpsEngine"),
    ("cdn-edge-agent", "cdn_edge", "CdnEdgeEngine"),
    ("incident-ops-agent", "incident_ops", "IncidentOpsEngine"),
    ("cost-ops-agent", "cost_ops", "CostOpsEngine"),
    ("compliance-ops-agent", "compliance_ops", "ComplianceOpsEngine"),
    ("secrets-ops-agent", "secrets_ops", "SecretsOpsEngine"),
    ("gitops-pilot-agent", "gitops_pilot", "GitopsPilotEngine"),
    ("edge-iot-agent", "edge_iot", "EdgeIotEngine"),
    ("perf-lab-agent", "perf_lab", "PerfLabEngine"),
    ("disaster-recovery-agent", "disaster_recovery", "DisasterRecoveryEngine"),
    ("migration-ops-agent", "migration_ops", "MigrationOpsEngine"),
]

def _load(slug, module, cls_name):
    path=os.path.join(AGENTS_DIR, slug, "core", f"{module}_engine.py")
    spec=importlib.util.spec_from_file_location(f"{slug}_{module}", path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, cls_name)

class TestComputer100Structure(unittest.TestCase):
    def test_exactly_one_hundred(self):
        self.assertEqual(len(COMPUTER100), 100)
        self.assertEqual(len({s for s,_,_ in COMPUTER100}), 100)
    def test_every_agent_has_skill_core_cli(self):
        for slug, module, _ in COMPUTER100:
            base=os.path.join(AGENTS_DIR, slug)
            self.assertTrue(os.path.isfile(os.path.join(base, "SKILL.md")), f"{slug}: SKILL.md")
            self.assertTrue(os.path.isfile(os.path.join(base, "core", f"{module}_engine.py")), f"{slug}: engine")
            self.assertTrue(os.path.isfile(os.path.join(base, "cli", f"{module}.py")), f"{slug}: CLI")
    def test_skill_md_frontmatter_parses(self):
        import yaml
        for slug, _, _ in COMPUTER100:
            content=open(os.path.join(AGENTS_DIR, slug, "SKILL.md"), encoding="utf-8").read()
            self.assertTrue(content.startswith("---"), f"{slug}: no frontmatter")
            meta=yaml.safe_load(content.split("---",2)[1])
            for key in ("name","description","version"):
                self.assertIn(key, meta, f"{slug}: missing {key}")
    def test_registry_discovers(self):
        sys.path.insert(0, REPO_ROOT)
        from core.registry import AgentRegistry
        agents=AgentRegistry.discover_agents()
        for slug,_,_ in COMPUTER100:
            self.assertIn(slug, agents, f"{slug} not discovered")

class TestComputer100CLIs(unittest.TestCase):
    def test_every_cli_help_from_neutral_cwd(self):
        failures=[]
        for slug, module, _ in COMPUTER100:
            cli=os.path.join(AGENTS_DIR, slug, "cli", f"{module}.py")
            proc=subprocess.run([sys.executable, cli, "--help"], capture_output=True, text=True, timeout=60, cwd="/tmp")
            if proc.returncode!=0:
                failures.append((slug, proc.stderr.strip()[-200:]))
            elif "usage:" not in proc.stdout.lower():
                failures.append((slug, "no usage"))
        self.assertEqual(failures, [], f"CLI failures: {failures}")

class TestComputer100Engines(unittest.TestCase):
    def test_all_engines_analyze_and_format(self):
        for slug, module, cls_name in COMPUTER100:
            with self.subTest(agent=slug):
                Engine=_load(slug, module, cls_name)
                text=f"Sample for {slug}: linux macos windows browser terminal server automation with {slug.replace('-agent','').replace('-',' ')} and extra content to avoid thin check.\n- bullet: value\n- bullet2: value\nMore content for depth."
                result=Engine.analyze(text)
                self.assertIn(result.verdict, ["PASS","PASS_WITH_NOTES","NEEDS_REVIEW","BLOCKED","NEEDS_INPUT"])
                self.assertGreaterEqual(result.score, 0)
                self.assertLessEqual(result.score, 100)
                self.assertIn("detected_os", result.metrics)
                report=Engine.format_report(result)
                self.assertIn(result.verdict, report)

if __name__=="__main__":
    unittest.main()
