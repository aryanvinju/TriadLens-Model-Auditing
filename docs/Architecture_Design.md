# TriadLens: Software Architecture and Design Specification (IEEE-style)

Current verification (13 November 2026): the four contributor PRs are merged; 60 Python tests, two real-model Playwright cases, one public fixture, CI publication and the current-image Docker/Kubernetes checks pass. See [DevOps verification](DevOps_Verification.md) and [sprint execution](Sprint_Execution_and_Demo.md). Earlier dated status statements below are historical. Human review and student narration remain pending.


Version 1.3 | 3 November 2026
Project team: Aryan Vinju, Aditya Shetty, Avantika Jitesh, Apeksha Ashok. Student identifiers are kept in the private submission PDFs.

## 1. Introduction

This document designs the educational ML/DL/QML disagreement-audit portal defined in SRS v2.3. The design separates offline model training from online inference, retains one reproducible data split, and gives users enough evidence to recognize disagreement and class imbalance. The system is not a clinical decision system.

## 2. Architecture

### 2.1 Pattern and rationale

TriadLens uses a layered modular monolith for online serving plus an offline training pipeline. The browser talks to a Flask HTTP API. The API validates requests, applies saved preprocessing, calls one or more loaded model adapters, and returns JSON. The training pipeline runs separately and persists versioned model artifacts and evaluation reports. This avoids training during requests and keeps the classroom deployment small. Two Kubernetes replicas serve the same immutable artifacts; they do not share patient data or a database.

### 2.2 Three-tier logical architecture

```mermaid
flowchart LR
  subgraph Tier1[Presentation tier]
    Browser[HTML/CSS/JavaScript audit page]
    Flow[Input - processing - output view]
    Browser --> Flow
  end
  subgraph Tier2[Application tier]
    API[Flask HTTP API and validation]
    Audit[Prediction and disagreement audit]
    ML[ML, DL and simulated QML adapters]
    API --> Audit --> ML
  end
  subgraph Tier3[Data and artifact tier]
    Models[(Versioned model files)]
    Reports[(Metrics and split reports)]
    CSV[(Local survey CSV for offline training)]
  end
  Browser -->|JSON request| API
  API -->|JSON response| Browser
  Models --> ML
  Reports --> Audit
  CSV -->|offline train.py only| Models
  CSV -->|offline evaluation only| Reports
```

The presentation tier receives survey input and renders both the three-step test flow and audit output. The application tier validates 15 fields, loads preprocessing and model adapters, computes predictions and agreement, then returns JSON. The data/artifact tier consists of trusted local model files and evaluation reports, with the CSV used only during offline training. There is no database or stored user prediction history. In Kubernetes the application tier is replicated in two Pods and reads model/report artifacts from read-only mounts; the public Docker image carries source code only.

### 2.3 UML component diagram

```mermaid
flowchart LR
  CSV[(Survey CSV)] --> Train[«component» Training and Data Audit]
  Train --> Artifacts[(Model artifacts and metrics)]
  Browser[«component» Browser UI] -->|HTTPS / JSON| API[«component» Flask API]
  API --> Validate[«component» Input Validator]
  API --> Predict[«component» Prediction and Disagreement Audit]
  Predict --> ML[«component» Logistic Regression]
  Predict --> DL[«component» PyTorch Network]
  Predict --> QML[«component» Quantum Kernel SVM]
  Artifacts --> ML
  Artifacts --> DL
  Artifacts --> QML
  Artifacts --> Predict
```

The browser has no access to model files. The validator owns field/type constraints. The prediction component selects ML, DL, QML or ALL, and computes an agreement audit only for ALL. The quantum circuit is simulated exactly with NumPy on a CPU; the SVM is classical.

### 2.4 Deployment view

```mermaid
flowchart LR
  User[Browser] --> Service[Kubernetes Service :80]
  Service --> Pod1[Pod 1: Gunicorn + Flask]
  Service --> Pod2[Pod 2: Gunicorn + Flask]
  CI[GitHub Actions] --> Hub[Docker Hub source-only image]
  Hub --> Image[Docker image]
  Image --> Pod1
  Image --> Pod2
  Secrets[Local cluster model and report Secrets] --> Pod1
  Secrets --> Pod2
```

The Dockerfile uses a non-root user, Gunicorn, and port 5000. The Docker context excludes the survey CSV, model artifacts and detailed reports. GitHub Actions builds that source-only image on pushes and pull requests; [main run 43279363986](https://github.com/aryanvinju/TriadLens-Model-Auditing/actions/runs/43279363986) published its SHA and latest tags to Docker Hub. The Kubernetes Deployment requests CPU/memory, sets limits, drops Linux capabilities, uses a read-only root filesystem and mounts a small writable `/tmp` plus read-only model/report Secrets. Startup/readiness probes call `/health/ready`; liveness calls `/health/live`. The current-image Docker Desktop rollout, Service request and 2/3/2 scaling passed on 13 November 2026. Earlier Pod replacement evidence is historical.

### 2.5 Functional requirement-to-test traceability matrix

| FR | Main design element | Verification case |
|---|---|---|
| FR01 | Browser form with 15 fields | ST01, ST16, PW02 |
| FR02 | Filtered `/api/example` and browser sampling | ST28, PW01 |
| FR03 | Exact request schema validator | ST06 |
| FR04 | Feature type and range validator | ST05, ST09 |
| FR05 | Model selection and adapters | ST03, ST04, PW01 |
| FR06 | Result labels, score types and timings | ST03, ST04, ST16, PW01 |
| FR07 | QML margin description | ST03, ST16, PW01 |
| FR08 | Saved metrics and `/api/metrics` | ST13 |
| FR09 | Seeded disjoint split | ST10 |
| FR10 | Training-only preprocessing | ST04, ST10 |
| FR11 | API error handling | ST07, ST08 |
| FR12 | Liveness and readiness | ST02, ST08 |
| FR13 | Two-Pod Deployment and Service | ST18, ST19 |
| FR14 | Model and evaluation artifact saving | ST04, ST10, ST13 |
| FR15 | Case agreement and held-out audit | ST24, ST25, ST27, PW01 |
| FR16 | Actions publish to Docker Hub | ST26 |
| FR17 | Age and gender-code slices | ST28, PW01 |
| FR18 | One-field sensitivity endpoint and view | ST29, PW01 |
| FR19 | Saved-label and session comparison | ST28, PW01 |
| FR20 | Browser input-processing-output flow | PW01 real-model flow; PW02 data-free UI fixture |

ST cases are defined in the [System Test Plan](System_Test_Plan.md). PW01 and PW02 are Playwright browser cases; PW02 mocks API responses and verifies presentation behavior only. Nonfunctional and security requirements map to ST04-ST21 and the CI/operational checks in the test plan. Prior Docker Hub and Kubernetes checks apply to the October image; the new revision requires another remote run before deployment acceptance.

### 2.6 Security architecture

The API accepts a JSON object with exactly `model` and `features`, rejects unknown fields, enforces types and ranges, and limits payloads to 16 KiB. Serialized model files come from trusted local mounts or Kubernetes Secrets, not the public image. Survey inputs are not persisted. Responses use no-store caching, nosniff, and a same-origin Content Security Policy. The image runs as UID 10001 and the manifest drops capabilities. The service must be exposed through HTTPS for any networked demonstration; the local port-forward is intended for a lab environment.

## 3. Detailed design

### 3.1 Data and model pipeline

The input CSV has 309 rows and 16 columns. The pipeline strips column whitespace, removes 33 exact duplicates, and excludes two contradictory-label rows. The remaining 274 rows are stratified with seed 42 into 175 training, 44 validation and 55 held-out test rows. StandardScaler, PCA and angle scaling are fitted on training records only. Logistic regression uses balanced class weights. The PyTorch network has 15 inputs, two ReLU hidden layers (32 and 16 units) and one output logit; validation loss selects its checkpoint. QML maps four PCA components to a four-qubit RY/RZ/CNOT statevector, computes a fidelity kernel, and fits a classical SVM. The test partition is used only for final evaluation.

### 3.2 UML sequence diagram: all-model comparison

```mermaid
sequenceDiagram
  actor Student
  participant UI as Browser UI
  participant API as Flask API
  participant V as Validator
  participant M as Loaded model adapters
  Student->>UI: Enter 15 features and choose ALL
  UI->>API: POST /api/predict JSON
  API->>V: Validate exact schema and feature codes
  alt Invalid
    V-->>API: Validation error
    API-->>UI: 400 JSON error
  else Valid
    V-->>API: Normalized features
    API->>M: Predict ML, DL, QML
    M-->>API: Three labels and scores
    API->>API: Count agreement; flag disagreement/extrapolation
    API-->>UI: Results, comparison, warnings
  end
  UI-->>Student: Show model results and agreement audit
```

### 3.3 UML sequence diagram: train and publish artifacts

```mermaid
sequenceDiagram
  actor Operator
  participant T as train.py
  participant D as CSV and split logic
  participant M as Three model trainers
  participant R as Artifacts/reports
  Operator->>T: python train.py
  T->>D: Audit, clean, stratify seed 42
  D-->>T: Train, validation, test IDs
  T->>M: Fit preprocessing and ML/DL/QML on train
  M-->>T: Trained models; DL validation checkpoint
  T->>M: Evaluate once on held-out test
  M-->>T: Predictions and scores
  T->>R: Save models, split IDs, metrics, predictions
  R-->>Operator: Reproducible evidence files
```

### 3.4 API contracts

| Method/path | Input | Output or error |
|---|---|---|
| GET `/` | None | Browser interface |
| GET `/api/example` | Optional `kind` and `exclude` query | One random held-out record and saved label when private test evidence is mounted; otherwise the training example |
| GET `/api/metrics` | None | Saved split and model metrics; 503 if missing |
| GET `/api/audit` | None | Aggregate cleaning, error, agreement and slice audit; no row-level records |
| POST `/api/predict` | `{model: ML|DL|QML|ALL, features: 15 fields}` | `results`, `comparison`, `warnings`, `note` |
| POST `/api/audit/sensitivity` | `{features: 15 fields}` | Label flips across one-field variations |
| GET `/health/live` | None | 200 if process responds |
| GET `/health/ready` | None | 200 if all artifacts load, otherwise 503 |

Each result includes `model`, YES/NO dataset `label`, numeric `score`, `score_type`, illustrative `risk` metadata and `inference_ms`. The QML score is an SVM margin, not a probability. The `comparison` object is null for individual model selection; for ALL it includes per-model labels, agreement_count, unanimous, majority_dataset_label, review_flag and review_reasons. The majority label is descriptive and is not used to change any model output.

### 3.5 Error handling and boundaries

400 indicates invalid JSON structure or feature value; 405 unsupported method; 413 oversized body; 415 wrong content type; 503 missing model/metric artifacts. Unexpected errors are logged server-side and returned as a generic 500 response without a stack trace. An age outside the training range is accepted when within the API range but produces a warning and review flag. There is no persistence of individual survey submissions.

### 3.6 Design limits

Only 55 cleaned records form the test set, including seven NO labels, so the reported metrics are unstable and are not clinical validation. QML uses four PCA dimensions whereas ML and DL use 15 inputs. The simulator does not run on quantum hardware or demonstrate a speed advantage. The local CSV provenance and binary-code meanings are not verified. No authentication is provided because the prototype does not store user accounts or prediction histories.

## 4. Change control and verification

Changes to preprocessing require retraining all three models, updating split/metric reports, and rerunning tests. Changes to the disagreement rule require updates to FR15, ST24–ST25, the API contract and the browser panel. Git tracks reviewed source changes; GitHub hosts the pull request. GitHub Actions runs checks and builds the source-only image for pushes and pull requests, then publishes to Docker Hub from main when checks pass. The Kubernetes image reference must be set to its published SHA tag.

