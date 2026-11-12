# TriadLens: ML, DL and QML Disagreement Audit
# System Test Plan and Execution Record (IEEE 829-style)

Version 2.2 | 3 November 2026

Project team: Aryan Vinju, Aditya Shetty, Avantika Jitesh, Apeksha Ashok. Student identifiers are in the private submission PDFs.
Tester: project team
Instructor review: pending

**Test plan identifier:** TL-TP-2026-02. IEEE 829-2008 is a test-documentation standard, not an SRS standard. The SRS uses ISO/IEC/IEEE 29148-style requirements structure. This plan retains the existing ST case IDs and covers the IEEE 829 plan elements below; it does not claim formal standards certification.

| IEEE 829 plan element | Location in this document |
|---|---|
| Identifier and introduction | Header and Section 1 |
| Test items and environment | Section 2 |
| Features to test / not test | Sections 3-4 |
| Approach and cases | Section 5 and Section 6 |
| Pass/fail and suspension/resumption | Section 8 and Section 9 |
| Test deliverables and tasks | Section 9 |
| Environmental needs, responsibilities and staffing | Sections 2 and 9 |
| Schedule, risks and contingency | Section 9 |
| Approvals | Section 9 |

## 1. Objective and scope

Verify the full-stack prediction flow, all three models, disagreement audit, educational risk bands, input validation, data separation, quantum simulator correctness, GitHub Actions, Docker Hub publication and Kubernetes deployment. This plan covers software behavior, not clinical validation or quantum advantage.

## 2. Test items and environment

Windows with Python 3.13 and the versions recorded in reports/metrics.json. Use the supplied lungcancer.csv, trained artifacts and held-out prediction evidence. The cleaned dataset has 274 records: 175 train, 44 validation and 55 test. Seed 42 is used for stratified splitting. Docker and a selected Kubernetes context are additional prerequisites for deployment tests.

## 3. Features to be tested

Dataset cleaning, training-only preprocessing, ML/DL/QML inference, disagreement flags, slice and sensitivity audits, random held-out sampling, input-processing-output browser flow, API validation, frontend assets, health endpoints, privacy headers and deployment configuration. The relevant SRS IDs are FR01–FR20, NFR01–NFR10 and SR-01–SR-04.

## 4. Features not to be tested

Clinical diagnosis, institutional identity systems, patient records, quantum hardware advantage and production availability are outside the project scope.

## 5. Approach, cases and actual results

Case identifiers map directly to tests/test_system.py. Parameterized variations account for the total number of tests.

| ID | Procedure and expected outcome | Requirement | Status |
|---|---|---|---|
| ST01 | Request page, CSS and JavaScript; all return 200. | FR01 | PASS |
| ST02 | With model artifacts loaded, liveness and readiness succeed. | FR12 | PASS |
| ST03 | Select ML, DL, QML and ALL; return only the selected models, finite scores and labels. | FR05 to FR07 | PASS |
| ST04 | Submit all 55 held-out records; all 165 model labels match saved predictions and scores match within 1e-6. | FR05, FR10, NFR01 | PASS |
| ST05 | Reject 13 invalid age, gender and binary-code variations with 400. | FR04 | PASS |
| ST06 | Reject six missing/extra field, malformed-schema and invalid-model variations with 400. | FR03 | PASS |
| ST07 | Wrong content type, malformed JSON, oversized payload and wrong method yield 415, 400, 413 and 405. | FR11, NFR02 | PASS |
| ST08 | Missing model files leave liveness at 200 but readiness and prediction at 503. | FR11, FR12, NFR06 | PASS |
| ST09 | An accepted age outside training coverage produces an extrapolation warning. | FR04 | PASS |
| ST10 | Verify cleaning audit, disjoint/exhaustive splits and training-only scaler fitting. | FR09, FR10, FR14 | PASS |
| ST11 | Verify known Bell-state preparation and cancellation of two identical CNOT gates. | QML design | PASS |
| ST12 | Verify state normalization, symmetric positive-semidefinite fidelity kernel, unit diagonal and zero-angle circuit state. | QML design | PASS |
| ST13 | Recompute metrics and confusion matrices from saved test predictions; match API report. | FR08, FR14 | PASS |
| ST14 | Check no-store caching and same-origin content security policy. | NFR03 | PASS |
| ST15 | Repeated requests produce identical labels and scores. | NFR05 | PASS |
| ST22 | Test 15 score-band cases, including exact boundaries for ML/DL and QML. | Educational risk levels | PASS |
| ST23 | API risk metadata matches its model and score; clinical_risk remains false. | Educational risk levels | PASS |
| ST24 | Synthetic label combinations produce the correct agreement count, majority label and review reasons. | FR15 | PASS |
| ST25 | ALL returns an audit matching model outputs; a single-model request returns null audit. | FR15 | PASS |
| ST27 | Held-out audit reports 49 unanimous and 6 disagreement cases; pairwise counts and QML false positives match saved predictions and confusion matrices. | FR15 | PASS |
| ST28 | Slice counts cover all 55 test records; random examples reference actual held-out rows, avoid an excluded row, and support disagreement and shared-error filters. | FR02, FR17 | PASS |
| ST29 | A complete record produces 16 one-field probes; reported flip counts equal changed-case entries and invalid features are rejected. | FR18 | PASS |

The 14 October local automated result was **60 passed, zero failures, zero errors**. The suite was repeated on **2 November 2026** with `python -m pytest -q --basetemp=tmp/pytest-submission-20261102`: **60 passed in 8.05 seconds**. Four checks are data-free public CI checks. JUnit evidence for the earlier 57-test run is in the private submission bundle at reports/test_results.xml. JavaScript syntax also passed on 2 November. Timings vary by machine.

On **3 November 2026**, Pytest again passed **60/60**; Pylint 4.1.3 with `--errors-only` passed on `app.py`, `audit.py`, `core.py`, `quantum.py` and `train.py`; JavaScript syntax passed. Playwright 1.62.1 with local Microsoft Edge passed **2/2 real-model browser cases** and **1/1 data-free fixture case**. The real browser test displays a held-out record through input, processing, output, disagreement, saved-label comparison, four aggregate slices and 16 one-field probes. The fixture test checks front-end rendering without private model files. These are local results; a GitHub Actions run for the current revision remains unverified.

### 5.1 Security validation

ST05–ST07 reject malformed fields, unexpected JSON keys, wrong content type and oversized bodies. ST14 checks no-store responses and the same-origin Content Security Policy. The Dockerfile and Kubernetes manifest are inspected for a non-root user, dropped capabilities and resource limits; live container and cluster validation passed ST18–ST19. These cases trace to SO-01–SO-03 and SR-01–SR-04 in the SRS.

## Risk band expectations

ML and DL: Low below 0.30; Moderate from 0.30 to below 0.70; High at or above 0.70. QML margin: Low below -0.50; Moderate from -0.50 to below 0.50; High at or above 0.50. These are illustrative thresholds chosen for the lab, not medically established thresholds. The original classification and raw score must remain unchanged. A Low level must not be described as ruling out disease. Levels across models are not directly comparable.

## 6. Manual and operational cases

| ID | Procedure | Expected outcome | Status |
|---|---|---|---|
| ST16 | In the browser, load an example, run ALL and each model, then submit a missing field. | Correct result cards and risk badges appear; required-input error is visible. | PASS: ALL, ML, DL and QML views showed the expected cards; missing Gender code showed a required-input prompt |
| ST17 | Use keyboard navigation, 375 px viewport and 200 percent zoom. | Focus and controls remain visible and usable. | PARTIAL PASS: Tab moved visible focus to Age; at 375 px there was no horizontal overflow and form/results remained usable; 200 percent zoom was not independently verified |
| ST18 | Pull the source-only image, mount local model/report files and run it on host port 5001. | Container becomes ready and all three models respond; image itself contains no private artifacts. | PASS: pulled SHA tag; unmounted image has no survey CSV or saved model files; mounted container returned ready and ML/DL/QML results |
| ST19 | Create local cluster Secrets, pull the image, apply YAML, wait for rollout and port-forward Service to 8080. | Two ready Pods and successful three-model HTTP response through Service. | PASS: Docker Desktop context, two ready Pods, ready endpoint and ML/DL/QML response through Service |
| ST20 | Scale to three replicas, verify readiness, then restore two. | Desired replica counts are achieved. | PASS: 3/3 ready, then 2/2 ready |
| ST21 | Delete one exact Pod in namespace lung-lab and observe replacement. | Replacement becomes ready; API works after reconnecting port-forward if needed. | PASS: deleted `lung-lab-855cc58c-hhtw2`; replacement `lung-lab-855cc58c-btg9m` became ready; API worked after reconnecting port-forward |
| ST26 | After repository secrets are configured, merge the reviewed PR or manually run the workflow on main. | GitHub Actions publishes SHA and latest tags to aryanvinju/se_miniproj; pulled image excludes survey rows and model artifacts. | PASS: [main run 38201577529](https://github.com/aryanvinju/SE_MINPROJ/actions/runs/38201577529) pushed both tags; pulled digest `sha256:ecbd5049e833911c3db2b09d0395d207a32797b2ef87b8235e233af3373d0e87`; image inspection confirmed exclusions |
| PW01 | Use Playwright with actual local artifacts: load a disagreement record, inspect input-processing-output, saved label, slices and sensitivity; reject missing required input. | Browser renders a real-model audit and blocks empty submission. | PASS locally on 3 November: 2/2 Edge cases; screenshot in local `test-results/input-processing-output.png` |
| PW02 | Use Playwright with a clearly mocked API fixture in public CI. | Browser passes 15 fields and renders three model labels and saved label without including private artifacts. | PASS locally on 3 November: 1/1 Edge case; remote CI pending |

Kubernetes YAML parsing and label-selector consistency were checked, followed by live Docker Desktop cluster deployment. Optional WebMCP integration has not been checked in a compatible browser and is outside lab acceptance.

## 7. Execution steps

From the project folder, run `python train.py`, then `python -m pytest -q --junitxml=reports/test_results.xml`. If the default temporary directory is inaccessible, add `--basetemp` with a new writable task-specific folder. Run `python -m pylint --errors-only app.py audit.py core.py quantum.py train.py` after installing Pylint 4.1.3. Run `npm ci` and install a Playwright browser; with local model artifacts available, start `python app.py` on port 5002 and run `npm run test:e2e` with `TRIADLENS_TEST_PORT=5002`. `npm run test:e2e:ci` executes the explicitly mocked data-free UI case. Start `python app.py`; use the README HTTP example. For operational cases follow the README Minikube commands only against the lab cluster and namespace.

## 8. Evidence, traceability and acceptance

Preserve test_results.xml, metrics.json, splits.json, test_predictions.csv and http_smoke_test.json. Capture actual browser results and real kubectl output when manual/operational checks are executed. Do not fabricate screenshots or mark blocked tests passed.

Local automated acceptance requires every automated test and a real HTTP smoke request to succeed. Full lab acceptance also requires ST16 through ST21, ST26, a remote GitHub Actions run, and instructor review. Current local Python, Pylint, JavaScript and Playwright checks pass. The dated Docker Hub and Docker/Kubernetes operational cases passed for an earlier image; the current revision has not been published or redeployed. The ST17 200 percent zoom check and instructor review remain open.

Traceability: FR/NFR links appear in the SRS and test tables. On failure, log evidence, fix and rerun; never tune on held-out data.

## 9. Remaining IEEE 829 plan elements and controls

**Pass/fail criteria.** A case passes only when its stated expected outcome is observed with a real command, browser interaction or inspection record. Automated suites require zero failures. A fixture case proves UI behavior only and is not evidence of real model performance. A remote deployment passes only for the exact commit and image tag tested.

**Suspension and resumption.** Suspend model-dependent cases when the dataset or artifacts are missing, browser cases when the browser cannot launch, and deployment cases when Docker or Kubernetes is unavailable. Record the reason as blocked, restore the prerequisite, then rerun the same case; do not mark it passed from an earlier result.

**Deliverables and tasks.** Keep this plan, the requirement-to-test matrix in the architecture document, Pytest/JUnit output, Playwright HTML report and screenshots, Pylint output, HTTP smoke results, GitHub Actions run URL, Docker Hub immutable tag, and Kubernetes rollout/pod/service evidence. Tasks are to prepare artifacts, run suites, review failures, retest fixes, and sign off the exact revision.

**Environment, roles and training.** The lab needs Python 3.13, pinned Python packages, Node.js 22, Playwright 1.62.1 with Chromium or Edge, Pylint 4.1.3, a browser, and, for deployment cases, Docker plus a selected Kubernetes cluster. A test executor records results; a reviewer checks evidence and deviations. Teammate ownership is assigned in the new repository only after each person reviews and commits their actual work. Team members must know the input schema and that QML is CPU-simulated.

**Schedule, risks and contingency.** Original Sprint 1 and Sprint 2 dates were 19-23 and 26-30 October 2026. Verification on 3 November is a later check, not a backdated sprint result. Small, imbalanced data limits interpretation; unavailable private artifacts prevent public CI from running the full suite; missing Docker/Kubernetes prevents a fresh deployment check. The contingency is to run the data-free public checks in CI and retain full model/deployment verification as separate, dated evidence.

**Approvals.** Test executor: project team; instructor acceptance: pending. Do not mark final acceptance or a sprint freeze until current-revision CI, deployment and review evidence has been attached.

