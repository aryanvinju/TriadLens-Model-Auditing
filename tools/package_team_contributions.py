"""Create four non-overlapping, source-only team handoff archives."""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "output" / "team_handoff"

PACKAGES = {
    "01-data-models": (
        "core.py", "train.py", "data/README.md", "models/README.md",
        "reports/README.md", "reports/dl_training_history.csv",
    ),
    "02-api-qml": (
        "app.py", "audit.py", "quantum.py",
    ),
    "03-ui-browser": (
        "templates/index.html", "static/app.js", "static/style.css",
        "package.json", "package-lock.json", "playwright.config.js",
        "tests/e2e/audit.spec.js", "tests/e2e/public.spec.js",
    ),
    "04-quality-devops-docs": (
        ".dockerignore", ".gitattributes", ".gitignore",
        ".github/workflows/ci.yml", "Dockerfile", "README.md",
        "k8s/lung-lab.yaml", "requirements.txt", "pytest.ini", "run_lab.cmd",
        "tests/test_public.py", "tests/test_system.py",
        "docs/Architecture_Design.md", "docs/DevOps_Verification.md",
        "docs/Originality_and_Demo.md", "docs/Product_Backlog_and_Two_Sprints.md",
        "docs/SRS.md", "docs/System_Test_Plan.md",
        "docs/Sprint_Execution_and_Demo.md", "docs/Team_Handoff_and_Test_Plan.md",
        "docs/build_pdfs.py", "docs/diagrams/use_case.svg",
        "tools/package_team_contributions.py",
    ),
}

OWNER = {
    "01-data-models": "Aryan Vinju",
    "02-api-qml": "Aditya Shetty",
    "03-ui-browser": "Avantika Jitesh",
    "04-quality-devops-docs": "Apeksha Ashok",
}


def main() -> None:
    seen: set[str] = set()
    for name, paths in PACKAGES.items():
        for relative in paths:
            if relative in seen:
                raise ValueError(f"Path appears in multiple archives: {relative}")
            seen.add(relative)
            if not (ROOT / relative).is_file():
                raise FileNotFoundError(ROOT / relative)

    DEST.mkdir(parents=True, exist_ok=True)
    for name, paths in PACKAGES.items():
        target = DEST / f"TriadLens_{name}.zip"
        note = (
            f"TriadLens handoff: {name}\n"
            f"Proposed reviewer/committer: {OWNER[name]}\n"
            "Extract this ZIP into the same new repository root as the other three ZIPs.\n"
            "Review and modify the files before committing your actual contribution.\n"
            "This allocation does not establish original authorship of every line.\n"
            "The public ZIP excludes the private CSV, trained models and row-level reports.\n"
            "Read docs/Team_Handoff_and_Test_Plan.md after all four ZIPs are combined.\n"
        )
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(f"_handoff/{name}.txt", note)
            for relative in paths:
                archive.write(ROOT / relative, relative)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        print(f"{target.name}\t{len(paths)} source files\tsha256:{digest}")


if __name__ == "__main__":
    main()
