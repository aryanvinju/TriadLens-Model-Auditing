# TriadLens team handoff and verification plan

Current verification (13 November 2026): the four contributor PRs are merged; 60 Python tests, two real-model Playwright cases, one public fixture, CI publication and the current-image Docker/Kubernetes checks pass. See [DevOps verification](DevOps_Verification.md) and [sprint execution](Sprint_Execution_and_Demo.md). Earlier dated status statements below are historical. Human review and student narration remain pending.


Version 1.0 | 3 November 2026

## Goal and sequence

1. Agree on the SRS and test-plan changes. The SRS follows ISO/IEC/IEEE 29148-style requirements headings; the test plan follows IEEE 829-style test-documentation headings. The architecture document contains a three-tier diagram and one FR-to-test row for every FR01-FR20.
2. Assemble the four non-overlapping source ZIPs in a new GitHub repository initialized with a README. Each proposed owner reviews and modifies their allocated files, then commits their actual work under their own account. The ZIP names are handoff boundaries, not proof that a person authored every original line.
3. Add the instructor-provided `data/lungcancer.csv` locally, run `python train.py`, and keep the generated row-level data, model artifacts and detailed reports out of the public repository. Run Pytest, Pylint, JavaScript syntax and Playwright against the assembled application.
4. Open pull requests for review. GitHub Actions runs public Pytest, Pylint, JavaScript, a data-free Playwright browser fixture, a source-only Docker build and an image import check. After review and merge to `main`, a successful workflow publishes the image to Docker Hub using repository secrets.
5. Pull the exact SHA-tagged Docker Hub image, mount trusted private model/report artifacts, and verify readiness and prediction. Deploy that tag to the local Kubernetes cluster, confirm two ready Pods and the Service response, then record demo/video evidence and the exact commit SHA.

The assembled repository is https://github.com/aryanvinju/TriadLens-Model-Auditing. PRs #1, #13, #14 and #15 contain all four contributions; CI run 43279363986 passed. Do not backdate these actions or use another person's account to commit.

## Proposed four-way file ownership

| ZIP | Proposed reviewer/committer | Contents and review focus |
|---|---|---|
| 01-data-models | Aryan Vinju | Data cleaning, shared feature schema, reproducible split, ML/DL training and training reports. |
| 02-api-qml | Aditya Shetty | Quantum simulator, Flask prediction API, validation boundary and aggregate audit. |
| 03-ui-browser | Avantika Jitesh | Barebones HTML/CSS/JS, input-processing-output view and Playwright browser checks. |
| 04-quality-devops-docs | Apeksha Ashok | Pytest cases, requirements and tooling, Docker/Actions/Kubernetes, SRS, architecture, test plan and handoff documentation. |

These are suggested review areas; the team must record real assignments and contributions. The package script checks that no source path is in more than one ZIP. The four ZIPs must be extracted into the **same repository root** before the application is run; individual ZIPs are intentionally not standalone applications.

## New repository integration procedure

Create one **new GitHub repository with an initial README** under Aryan's account, then invite the other three teammates as collaborators. Everyone accepts the invitation. The initial README gives `main` a commit so the first contributor can create a branch and PR. Do not add the private dataset yet.

Merge contributions in order: 01 data/models, 02 API/QML, 03 UI/browser, 04 quality/DevOps/docs. Each person clones the new repository **after the previous PR has merged**, creates a fresh branch from current `main`, extracts only their ZIP at the repository root, reviews and modifies their files, commits under their own Git identity, pushes the branch and opens a PR. The repository owner or another teammate reviews and merges it. The initial README is intentionally replaced by ZIP 04's project README. The first three branches are incomplete project slices; run the full checks after ZIP 04 has been added. A contributor should make and explain a genuine change to their package; the ZIP allocation does not establish authorship of every line.

Example PowerShell steps for **each contributor**, replacing the repository URL, branch and ZIP path with their own values:

```powershell
git clone https://github.com/aryanvinju/NEW_REPO.git
cd NEW_REPO
git switch -c contribution/03-ui-browser
Expand-Archive -LiteralPath 'C:\path\to\TriadLens_03-ui-browser.zip' -DestinationPath . -Force
git status --short
git add .
git commit -m "Add reviewed UI and browser tests"
git push -u origin contribution/03-ui-browser
```

Set `git config user.name "Your Name"` and `git config user.email "your verified GitHub email"` in the clone before committing if Git does not already identify you correctly. The person using ZIP 04 must inspect the replaced `README.md` and `.gitignore` before `git add .`. Open **Pull requests → New pull request**, choose the contribution branch against `main`, describe the actual work and tests, request a teammate review, and merge only after the checks available for that branch pass. Repeat from a fresh clone or `git switch main; git pull` for the next person. Never share one GitHub login or rewrite commit authors.

Before ZIP 04 merges, the repository owner adds `DOCKERHUB_USERNAME` (`aryanvinju`) and `DOCKERHUB_TOKEN` as **repository Actions secrets** in the new repository. The final main-branch push runs the Actions workflow and attempts publication to `aryanvinju/se_miniproj`; verify the test, browser-test, container and publish jobs. If the secret was added later, rerun the workflow on `main` and verify the result. The Kubernetes manifest still names an older published image; for the demonstration, apply the manifest and then run `kubectl set image deployment/lung-lab web=aryanvinju/se_miniproj:<full-new-commit-sha> -n lung-lab` before rollout verification. Record the exact SHA tag used. Do not copy `.private_submission.txt`, the survey CSV, model `.joblib`/`.pt` files, row-level predictions or private metric JSON into the public repository.

## Verification matrix

| Layer | Input | Processing | Visible output / evidence |
|---|---|---|---|
| Browser UI | 15 survey fields or sampled held-out case | JavaScript builds request and displays API response | Input-processing-output panel, three labels, saved-label comparison and session row |
| API | Exact JSON schema | Validation, saved preprocessing, ML/DL/QML inference, disagreement audit | JSON results, warnings, review reasons and status codes |
| Pytest | Fixed sample records and invalid variants | Direct Python and Flask test-client execution | 60 local tests passed on 3 November 2026 |
| Playwright real-model | Browser loads a real disagreement case | Browser to local Flask to three saved models | 2 local Edge cases passed; screenshot in `test-results/` |
| Playwright public fixture | Static fixture, with API responses explicitly mocked | Browser JavaScript rendering only | 1 local Edge case passed; suitable for data-free CI |
| Pylint | Python source | Error-class static analysis | `python -m pylint --errors-only ...` passed locally on 3 November |
| GitHub Actions | PR or push | Pytest, Pylint, Node syntax, Playwright fixture, Docker build | PASS: main run 43279363986 |
| Docker Hub / Kubernetes | SHA-tagged source-only image plus private mounts | Container startup, probes and two-replica Service routing | PASS: current SHA image verified on 13 November, including 2/3/2 scaling |

## Commands after assembly

```powershell
python -m pip install -r requirements.txt
python -m pip install pylint==4.1.3
npm ci
npx playwright install chromium
python train.py
python -m pytest -q
python -m pylint --errors-only app.py audit.py core.py quantum.py train.py
node --check static/app.js
$env:PORT='5002'; python app.py
```

In a second terminal, with the server running: ` $env:TRIADLENS_TEST_PORT='5002'; npm run test:e2e `. On Windows with installed Edge, set `$env:PLAYWRIGHT_USE_EDGE='1'` before the browser test. `npm run test:e2e:ci` runs only the data-free fixture. The README and DevOps verification document contain Docker and Kubernetes commands. Browser and container checks must be repeated for the new repository's exact commit.

## Presentation and completion evidence

Show the real browser input-processing-output flow, aggregate disagreement and slice audit, one-field sensitivity, the Pytest/Pylint/Playwright results, reviewed PRs, Actions run, Docker Hub tag and two ready Kubernetes Pods. Then show the requirement-to-test matrix. The project is complete for submission only when the new repository links, real PR reviews, current CI/image/cluster checks, and student-recorded sprint videos have been added to the execution record.
