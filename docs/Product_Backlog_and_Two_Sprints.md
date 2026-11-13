# TriadLens product backlog and two-sprint plan

Status checked 13 November 2026. [Repository](https://github.com/aryanvinju/TriadLens-Model-Auditing) and [Project board](https://github.com/users/aryanvinju/projects/2/views/1).

Team: Aryan Vinju (@aryanvinju), Aditya Shetty (@AdityaShetty-1), Avantika Jitesh (@avanthikajitesh), Apeksha Ashok (@apekshaashok). Student IDs are supplied separately in the private submission.

## Product backlog

| Issue | Backlog item | FR/NFR trace | Points | Sprint | Owner |
|---|---|---|---:|---|---|
| [#2](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/2) | Clean survey and reproducible split | FR09, FR10, FR14; NFR05 | 3 | 1 | @aryanvinju |
| [#3](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/3) | ML baseline and held-out metrics | FR05, FR08, FR14; NFR01 | 3 | 1 | @aryanvinju |
| [#4](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/4) | Validated prediction API and health | FR03, FR04, FR11, FR12; NFR02, NFR03, NFR06 | 3 | 1 | @AdityaShetty-1 |
| [#5](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/5) | Survey form, sample and result | FR01, FR02, FR06; NFR04 | 3 | 1 | @avanthikajitesh |
| [#6](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/6) | CI, review and one-minute demo | NFR08, NFR09 | 3 | 1 | @apekshaashok |
| [#7](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/7) | DL shared-split evaluation | FR05, FR06, FR08, FR14; NFR01, NFR05 | 5 | 2 | @aryanvinju |
| [#8](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/8) | Simulated four-qubit kernel SVM | FR05, FR06, FR07, FR14; NFR01 | 5 | 2 | @AdityaShetty-1 |
| [#9](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/9) | Disagreement, slices and stability | FR15, FR17-FR20; NFR02, NFR05 | 3 | 2 | @AdityaShetty-1 / avanthikajitesh |
| [#10](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/10) | Docker Hub and Kubernetes | FR12, FR13, FR16; NFR06, NFR07, NFR09, NFR10 | 3 | 2 | @apekshaashok |
| [#11](https://github.com/aryanvinju/TriadLens-Model-Auditing/issues/11) | System tests, docs, demo and freeze | FR01-FR20; NFR01-NFR10 | 3 | 2 | @apekshaashok |

Total: 34 points. Sprint 1: 15 points; Sprint 2: 19 points. Each GitHub issue retains its acceptance checks. Implementation and verification are complete for the core features; team review and final acceptance remain open.

## Sprint 1 backlog

Original assignment window: 19-23 October 2026. Goal: a tested ML path from survey input to prediction. Issues #2-#6 cover cleaning, reproducible splits, logistic regression, API, browser and CI. Source contributions were actually merged on 11-12 November; this is late execution against the planned scope.

Verification on 13 November: 175/44/55 disjoint records; held-out ML metrics recomputed; API validation and health tests pass; real browser flow passes. CI run 43279363986 passes public checks. The one-minute current-product scope demonstration is supplied in the private submission at output/demo/sprint1-scope-20261113.webm. It is silent; the student should narrate or present it live. It does not establish an October sprint ceremony.

## Sprint 2 backlog

Original assignment window: 26-30 October 2026. Goal: DL/QML comparison, disagreement auditing and deployment. Issues #7-#11 cover DL, simulated QML, audit views, Docker Hub, Kubernetes, documents and submission.

Verification on 13 November: all 60 Python tests pass; real-model Playwright 2/2 and public fixture 1/1 pass; Docker and Kubernetes serve predictions from the published image; scaling 2 to 3 to 2 succeeds. The two-minute current-product scope demonstration is in output/demo/sprint2-scope-20261113.webm in the private submission. Human review, student narration and final acceptance/freeze remain pending.

## Definition of done and evidence

- SRS acceptance checks pass and the [FR-to-test matrix](Architecture_Design.md) traces the implementation.
- Actual contributor PR, test evidence and teammate review are linked on the issue.
- Demonstration files and deployment evidence are available to the evaluator.
- Team review records the accepted commit and any limitations.

Do not close review-dependent issues solely because a PR was merged. [Sprint execution](Sprint_Execution_and_Demo.md) and [DevOps verification](DevOps_Verification.md) record current evidence. Jira SCRUM-5 through SCRUM-14 are legacy planning records; their live statuses have not been checked in this verification. GitHub issues #2-#11 are the current backlog.
