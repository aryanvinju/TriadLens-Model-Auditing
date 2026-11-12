# TriadLens sprint execution and demonstration record

Status checked 2 November 2026. This document reports observed work against the two sprint backlogs. The planned dates were 19-23 October and 26-30 October 2026. It does not backdate work or treat an implemented feature as proof of a completed sprint review.

Update 3 November 2026: the browser now shows a simple input-processing-output flow. Two real-model Playwright browser cases, one clearly mocked public UI case, Pylint error checks and all 60 Pytest cases passed locally. The SRS, architecture matrix and IEEE 829-style test plan were revised. The four source handoff ZIPs are described in [Team Handoff and Test Plan](Team_Handoff_and_Test_Plan.md). These are later changes, not evidence that the October sprint reviews occurred.

Project team: Aryan Vinju, Aditya Shetty, Avantika Jitesh and Apeksha Ashok. Jira currently assigns the TriadLens stories to Aryan. The other members' GitHub identities and actual PR contributions have not been verified.

## 1. Product and sprint scope

The [product backlog](Product_Backlog_and_Two_Sprints.md) contains ten estimated, traceable stories worth 34 points. Sprint 1 contains GitHub issues #3-#7 (15 points): cleaned data and fixed splits, ML baseline, validated API, simple browser workflow, CI and a one-minute demo. Sprint 2 contains issues #8-#12 (19 points): DL, simulated QML, disagreement and slice audits, Docker Hub and Kubernetes verification, system review and a two-minute demo. The same ten work areas are tracked in Jira as SCRUM-5 through SCRUM-14. The duplicate SCRUM-15 is excluded from sprint totals.

## 2. Execution evidence

| Acceptance area | Observed evidence on 2 November | Status |
|---|---|---|
| Data and split | 309 source rows; 33 exact duplicates removed and 2 conflicting rows excluded; 274 clean rows split 175/44/55. | Implemented locally |
| ML, DL and QML | Three saved model artifacts load; the QML component is a four-qubit CPU simulation and its SVM margin is identified as a margin. | Implemented locally |
| Test-set evaluation | ML 92.7%, DL 92.7%, QML 89.1% accuracy on 55 held-out records; always-YES baseline 87.3%. The test set has 7 NO and 48 YES labels. | Implemented locally; small sample |
| Audit portal | Aggregate audit reports 6 disagreements and 2 shared-error records. Random held-out cases, label comparison, age/gender-code slices and one-field sensitivity are available. | Implemented locally |
| Automated verification | `python -m pytest -q --basetemp=tmp/pytest-submission-20261102` returned 60 passed in 8.05 seconds. `node --check static/app.js` passed. Live local `/health/ready` returned ready on port 5002. | Passed locally on 2 November |
| Git and GitHub | Local Git history and public GitHub repository exist. Earlier PRs #1 and #2 predate the scheduled sprints. Current audit/UI changes are not committed as of this check. | Sprint review evidence incomplete |
| GitHub Actions and Docker Hub | Earlier main-branch runs published source-only images to `aryanvinju/se_miniproj`; see the dated [DevOps verification](DevOps_Verification.md). The current revision has no verified remote run or published image. | Earlier revision verified; current revision pending |
| Docker and Kubernetes | The earlier Docker Desktop check used a mounted-model image and two ready Kubernetes Pods, Service prediction, scaling and Pod replacement. Docker daemon was unavailable and Kubernetes configuration unreadable in this session. | Earlier revision verified; current revision pending |
| Jira and recordings | SCRUM-5 through SCRUM-14 still show To Do. No Sprint 1 or Sprint 2 video was found in the repository. | Formal sprint acceptance pending |

These statuses separate software that runs from evidence that the scheduled sprint process was carried out. Passing tests does not prove teammate PR authorship, sprint review, video delivery or deployment of the latest source.

## 3. Sprint reviews and deviations

**Sprint 1 planned outcome:** an ML browser-to-API vertical slice with cleaned data, reproducible split and CI. The functionality is present in the local product. The one-minute dated recording, sprint-specific teammate PR and owner review were not found, and Jira remains To Do. Record this as an incomplete sprint review, not a completed sprint.

**Sprint 2 planned outcome:** ML/DL/QML comparison, held-out audit, deployment verification, documentation, two-minute recording and frozen revision. The local product implements the model comparison and audits. Earlier deployment verification predates the latest audit changes. The recording, current-revision CI/publish/rollout, team review and freeze are unverified. The planned date has passed, so any later completion must be dated accurately.

**Deviation from the original scope:** feedback expanded the audit from a single comparison to random held-out case filters, aggregate errors, age/gender-code slices and one-field sensitivity (FR17-FR19). The current Markdown SRS, architecture and test plan describe this expansion; the PDF copies dated 12 October must be regenerated. The old Dockerfile omitted `audit.py` after this change; the Docker build context was corrected on 2 November. A successful container build is still required to verify that fix.

## 4. Demonstration to record and present

1. Open `http://127.0.0.1:5002/` on this computer. Show the audit summary: 55 held-out test records, 6 disagreements, 2 records every model got wrong and the majority baseline.
2. Under record audit choose **Model disagreement**, click **Load random record**, and compare the saved dataset label with ML, DL and QML outputs. Explain that QML shows an SVM margin, not a calibrated probability.
3. Choose **All models wrong** and load another record. Show the session comparison and review reasons. Run **Check one-field changes** and explain that it measures sensitivity, not causation.
4. Show the age and gender-code slices with their sample sizes. Avoid a fairness or medical claim based on these small groups.
5. Show the 60-test result, GitHub source and PR history, the GitHub Actions run and Docker Hub tag in the DevOps log, then show Jira. State that those deployment checks are for an earlier revision.

For the required recordings, capture the actual working screen and student narration. Suggested Sprint 1 cut: data and form (15 seconds), ML prediction and validation (25 seconds), tests/CI and issue link (20 seconds). Suggested Sprint 2 cut: aggregate audit (20 seconds), disagreement and shared-error cases (50 seconds), sensitivity and slices (25 seconds), current-revision CI/image/Pods if verified (15 seconds), remaining status and revision SHA (10 seconds). Add genuine file or accessible links to the backlog after recording. Do not substitute a script for a video.

## 5. DevOps chain and submission condition

Git versions the source; GitHub hosts the repository and PR reviews; GitHub Actions checks public tests and JavaScript, builds the source-only Docker image and publishes a successful main-branch image to Docker Hub; Docker packages the Flask application; Kubernetes runs two replicas with separately mounted private model/report artifacts and health probes. The image is not self-contained: a clean public checkout needs the dataset and training step, and a container needs the model/report mounts.

Before claiming final sprint completion, commit and review the actual changes, run remote CI for that commit, verify its Docker Hub SHA tag, pull and run that exact image with local artifacts, roll it out to Kubernetes, add the two genuine recordings, update Jira statuses with issue evidence, regenerate the SRS/architecture/test PDFs and record the frozen SHA. These are outstanding actions, not results claimed by this document.

## 6. Links

- Repository: https://github.com/aryanvinju/SE_MINPROJ
- Jira: https://pesuonline-team-g6ej69na.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog
- Docker Hub: https://hub.docker.com/repository/docker/aryanvinju/se_miniproj/general
- Earlier GitHub Actions main run: https://github.com/aryanvinju/SE_MINPROJ/actions/runs/38203946359
- Local SRS, architecture, test plan and dated DevOps verification: `docs/`
