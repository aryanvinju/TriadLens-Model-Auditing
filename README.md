# TriadLens: ML, DL and QML Model Auditing

TriadLens compares logistic regression, a PyTorch neural network and a simulated four-qubit quantum-kernel SVM on the same lung-survey split. It exposes model disagreement, saved-label errors, age/gender-code slices and one-field sensitivity. It is an educational audit portal; its outputs are not medical advice or calibrated cancer risk.

## Verified state - 13 November 2026

All four contributor packages are merged: PR #1 (Aryan), #13 (Aditya), #14 (Avantika), #15 (Apeksha). [Main CI](https://github.com/aryanvinju/TriadLens-Model-Auditing/actions/runs/43279363986) passed public tests, lint, browser fixture, Docker build and Docker Hub publish. Full local verification passed 60 Python tests, two real-model browser cases and one public fixture. The exact published image was pulled and served ML/DL/QML predictions through Docker and Kubernetes. Scaling 2 to 3 to 2 succeeded.

Human teammate review, student narration and final acceptance remain open. See [backlog](docs/Product_Backlog_and_Two_Sprints.md), [execution record](docs/Sprint_Execution_and_Demo.md) and [DevOps evidence](docs/DevOps_Verification.md).

## Setup and run

Use Python 3.13. Place the supplied private CSV at data/lungcancer.csv; see [data setup](data/README.md). Do not upload the dataset or serialized model artifacts to the public repository.

```powershell
python -m pip install -r requirements.txt
python train.py
python app.py
```

Open http://127.0.0.1:5000 (or the printed port). Load a random held-out record; inspect the input, processing, predictions, saved label and review reasons. Choose disagreement or all-models-wrong cases and run Check one-field changes. Session comparisons last until page refresh.

Training removes 33 duplicates and two contradictory rows from 309 records, yielding 274 records split 175/44/55 with seed 42. Preprocessing is fit only on training data. ML/DL/QML test accuracy is 92.7%/92.7%/89.1%, against an 87.3% majority baseline on 55 cases. Seven test labels are NO and 48 YES; small groups limit interpretation. QML uses four PCA components and exact CPU simulation, while ML/DL use 15 features. Its SVM margin is not a probability.

## Tests

```powershell
New-Item -ItemType Directory -Force tmp
python -m pytest -q --basetemp=tmp/local-tests
python -m pip install pylint==4.1.3
python -m pylint --errors-only app.py audit.py core.py quantum.py train.py
node --check static/app.js
npm ci
npx playwright install chromium
npm run test:e2e
npm run test:e2e:ci
```

On Windows, set PLAYWRIGHT_USE_EDGE=1 to use installed Edge. The public CI fixture mocks API responses; the real-model tests require trusted local artifacts. Public CI intentionally excludes the private dataset and derived evidence. Only load trusted serialized models. Local verification used NumPy 2.2.6; container requirements pin 2.3.3. Both prediction environments were exercised.

## Docker, Docker Hub and Kubernetes

Image: aryanvinju/se_miniproj:bf87c5b096b54de26ce6fcf651bc28eeb253d3a7. It contains source and dependencies; runtime model/report mounts are required. The manifest uses this verified tag, two replicas, readiness/liveness/startup probes and private artifact Secrets.

After starting Docker Desktop and its Kubernetes cluster, run powershell -File tools/verify_deployment.ps1. This starts a named local verification container, provisions local cluster artifact Secrets, deploys the image, tests readiness/prediction and scales 2/3/2. Detailed evidence is written under output/verification. See the script and [DevOps record](docs/DevOps_Verification.md) before rerunning against an existing named container.

## Submission

Editable documents are in docs: SRS, Architecture_Design (three-tier diagrams and FR-to-test matrix), System_Test_Plan (IEEE 829-style), Product_Backlog_and_Two_Sprints, Sprint_Execution_and_Demo, and DevOps_Verification. Generate PDFs with python docs/build_pdfs.py. IEEE 829 concerns test documentation; the SRS follows a 29148-style structure.

The private output/demo folder holds silent 60-second and 120-second current-product demonstrations. Add student narration or present them live. These November recordings do not establish October sprint ceremonies. tools/record_demos.cjs reproduces recordings with installed Edge and a full FFmpeg executable specified by FFMPEG_PATH.

The private submission ZIP includes source, PDFs, evidence, videos, CSV and freshly trained models. It is intended for the evaluator and must not be committed publicly. The accepted final revision is recorded by the team after review.
