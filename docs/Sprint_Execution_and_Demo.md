# TriadLens sprint execution and demonstration record

Updated 13 November 2026. Original planned windows: Sprint 1, 19-23 October; Sprint 2, 26-30 October. Contributions were merged on 11-12 November and current verification was performed on 13 November. Record this as late execution of the planned scope.

## Current execution evidence

| Area | Verified result | Evidence |
|---|---|---|
| Contributor assembly | All four packages merged | PR #1 Aryan; #13 Aditya; #14 Avantika; #15 Apeksha |
| Training and splits | Fresh ML/DL/QML artifacts, 175/44/55 disjoint records | train.py; local reports/metrics.json and splits.json |
| Evaluation | ML 92.7%, DL 92.7%, QML 89.1%; majority baseline 87.3% | 55 held-out records; 7 NO, 48 YES |
| Audit | Six disagreements, two shared errors; slices and 16 one-field probes | Full Python and real browser checks |
| Python/static checks | 60 passed; Pylint errors-only and Node syntax pass | output/verification/pytest.xml and lint log |
| Browser | Two real-model cases; one public fixture case pass | output/verification/playwright-full.txt and playwright-public.txt |
| CI/publication | All four jobs passed; SHA image published | [Main Actions run](https://github.com/aryanvinju/TriadLens-Model-Auditing/actions/runs/43279363986) |
| Deployment | Docker and Kubernetes predict with exact SHA image; 2/3/2 replicas | [DevOps verification](DevOps_Verification.md) |
| Human review | No submitted teammate review found | Team action required |

## Demonstrations and presentation

The private output/demo folder contains a 60-second Sprint 1 scope recording and a 120-second Sprint 2 scope recording made from the current product on 13 November. These are silent working-screen demonstrations, not historical recordings of October reviews. Add your own narration or present the videos live.

Sprint 1: explain the 15 survey inputs, random sample, single ML result, preprocessing, fixed split, held-out metrics and baseline. Show the passing CI link separately.

Sprint 2: explain aggregate errors and slices, load a disagreement case, compare ML/DL/QML with the saved label, load a shared-error case, inspect one-field stability and session comparisons. Explain that QML is an exact four-qubit CPU simulation and its SVM margin is not a probability. Show the Docker Hub SHA image and current Kubernetes evidence alongside the UI recording.

Run the portal with `python app.py`, or use the verified local Docker service on port 5003 and Kubernetes service on port 5005 while those processes remain running. These addresses are local to this computer.

## Submission and freeze

Verified application revision: `bf87c5b096b54de26ce6fcf651bc28eeb253d3a7`. The documentation/verification follow-up commit is the submission candidate; use its Git SHA in the final review record. No release freeze or instructor acceptance is claimed until the team records its approval. Keep the accepted source, PDFs, videos and private model/data package together.

Actual evidence and results should be attached to GitHub issues #2-#11. The [backlog](Product_Backlog_and_Two_Sprints.md) has corrected ownership and issue numbering. The new repository is [https://github.com/aryanvinju/TriadLens-Model-Auditing](https://github.com/aryanvinju/TriadLens-Model-Auditing); the GitHub Project board is https://github.com/users/aryanvinju/projects/2/views/1.
