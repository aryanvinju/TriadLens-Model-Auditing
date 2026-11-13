# TriadLens DevOps verification

Verified 13 November 2026 against application commit `bf87c5b096b54de26ce6fcf651bc28eeb253d3a7`. This record supersedes earlier deployment statements dated 12 October and 2-3 November.

## Git, GitHub and contributor PRs

The four merged contribution PRs are [#1](https://github.com/aryanvinju/TriadLens-Model-Auditing/pull/1) (Aryan, data/models), [#13](https://github.com/aryanvinju/TriadLens-Model-Auditing/pull/13) (Aditya, API/QML), [#14](https://github.com/aryanvinju/TriadLens-Model-Auditing/pull/14) (Avantika, UI/browser tests), and [#15](https://github.com/aryanvinju/TriadLens-Model-Auditing/pull/15) (Apeksha, quality/DevOps/docs). PR #12 was closed unmerged and superseded by #13. No submitted human reviews were found when checked on 13 November; a merge is not a review record.

## GitHub Actions and Docker Hub

[Main run 43279363986](https://github.com/aryanvinju/TriadLens-Model-Auditing/actions/runs/43279363986) passed test, browser-test, container and publish jobs. Public CI ran four Pytest checks, Pylint error checks, JavaScript syntax and one explicitly mocked Playwright browser flow. It built the image, imported app/audit, checked private artifact exclusions and published the SHA and latest tags.

Image: `aryanvinju/se_miniproj:bf87c5b096b54de26ce6fcf651bc28eeb253d3a7`.

Digest: `sha256:5f05c94b14817dbd64efebd3f9841cf298a80848f5b2a354ad905d1e6b1ccd31`.

The local pull returned that same digest. The unmounted image lacks lungcancer.csv, qml.joblib and metrics.json. Private artifacts are mounted separately.

## Full local verification

Models were regenerated from the local CSV with the merged train.py. Cleaning gives 274 records after 33 duplicate and two conflicting rows are removed; split counts are 175/44/55. All 60 Python tests passed in 6.30 seconds. Pylint error checks and JavaScript syntax passed. Installed Edge passed two actual-model browser cases and one public fixture case. Initial attempts encountered unavailable temporary-directory/browser paths; using a workspace temporary directory and installed Edge resolved those environment issues.

Local Python uses NumPy 2.2.6; the pinned container environment uses NumPy 2.3.3. The model and audit tests pass locally and the published container returns predictions. This does not establish a fresh Windows dependency installation.

## Docker runtime and Kubernetes

Docker container triadlens-verification-20261113 runs the exact SHA image on loopback port 5003 with read-only local models and reports. Readiness returns ready and POST /api/predict returns ML, DL and QML.

The docker-desktop cluster runs the same image in namespace lung-lab. The manifest specifies non-root execution, a read-only root filesystem, CPU/memory limits, health probes and read-only Secret mounts. Two new Pods became ready. Service port-forward on loopback port 5005 returns readiness and all three predictions. Scaling to three ready replicas and back to two succeeded. The final desired replica count is two.

Reproduce with `powershell -File tools/verify_deployment.ps1` after provisioning trusted local artifacts. Do not run it twice without first stopping/removing the previous named verification container. Local evidence is output/verification/deployment.json, image-digest.json, pods-two.json and pods-three.json. Those detailed machine artifacts remain in the private submission.

## Remaining human acceptance

Teammates must review the contribution/verification changes and record an acceptance decision. The team should provide its own narration and confirm the submitted revision. The original October sprint dates are retained as planned dates; November checks are not backdated.
