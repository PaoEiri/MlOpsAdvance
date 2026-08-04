# revolutionary-mlops

[![Lint](https://github.com/PaoEiri/MlOpsAdvance/actions/workflows/lint.yml/badge.svg)](https://github.com/PaoEiri/MlOpsAdvance/actions/workflows/lint.yml)
[![Tests](https://github.com/PaoEiri/MlOpsAdvance/actions/workflows/test.yml/badge.svg)](https://github.com/PaoEiri/MlOpsAdvance/actions/workflows/test.yml)
[![Validate Model](https://github.com/PaoEiri/MlOpsAdvance/actions/workflows/validate.yml/badge.svg)](https://github.com/PaoEiri/MlOpsAdvance/actions/workflows/validate.yml)
[![Live Report](https://img.shields.io/badge/live%20report-GitHub%20Pages-1D3557)](https://paoeiri.github.io/MlOpsAdvance/)

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![ruff](https://img.shields.io/badge/lint%2Fformat-ruff-D7FF64?logo=ruff&logoColor=black)
![ty](https://img.shields.io/badge/typing-ty-333333)
![GitHub Pages](https://img.shields.io/badge/deploy-GitHub%20Pages-222222?logo=githubpages&logoColor=white)

An end-to-end **MLOps CI/CD pipeline** built on GitHub Actions — from lint to a live metrics dashboard on GitHub Pages, with zero manual steps in between.

The "model" itself is intentionally a joke (a threshold classifier that predicts `TRUE` most of the time). The point of this project isn't the ML — it's the **automation pipeline** around it: a chained sequence of workflows that lints, tests, trains, validates, and deploys on every push, complete with quality gates and historical metrics tracking.

**Live report:** https://paoeiri.github.io/MlOpsAdvance/

## Highlights

- Fully automated, **5-stage CI/CD pipeline** with no manual triggers — each stage kicks off the next only on success (`workflow_run` chaining).
- Built-in **quality gate**: the pipeline fails the build if accuracy, precision, or recall drop below 80%.
- **Metrics history** persisted as JSON and committed back to the repo on every successful run, powering a trend chart over time.
- Automatic **HTML report generation and deployment to GitHub Pages** on every successful pipeline run — a live dashboard, not a static screenshot.
- Reusable **composite GitHub Action** (`.github/actions/setup-env`) to centralize Python/uv environment setup across workflows.
- Modern Python tooling: `uv` for dependency/env management, `ruff` for lint + format, `ty` for static typing, `pytest` for testing.

## Pipeline architecture

```
push → Lint → Tests → Train Model → Validate Model → Deploy (GitHub Pages)
```

Each stage is a separate GitHub Actions workflow, triggered by the successful completion of the previous one (`workflow_run`):

1. **Lint** — `ruff format --check` and `ruff check` on every push/PR to `main`.
2. **Tests** — runs the `pytest` suite once linting passes.
3. **Train Model** — trains the model and uploads the resulting `model_id` as a build artifact.
4. **Validate Model** — downloads the trained model, evaluates it against a validation set, and computes accuracy/precision/recall.
   - **Quality gate**: the pipeline fails if any metric drops below 80%.
   - Appends the run's metrics to a persisted JSON history (`.github/data/metrics_history.json`), committed back to the repo.
5. **Deploy** — generates an HTML report from the metrics history and publishes it to GitHub Pages via `actions/deploy-pages`.

## Tech stack

- **Language:** Python 3.14
- **Package/environment management:** [uv](https://github.com/astral-sh/uv)
- **CI/CD:** GitHub Actions (chained `workflow_run` pipelines, composite actions, environments, artifacts)
- **Testing:** pytest
- **Linting/formatting:** ruff
- **Static typing:** ty
- **Deployment:** GitHub Pages (`actions/upload-pages-artifact`, `actions/deploy-pages`)
- **Build backend:** hatchling

## Requirements

- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

## Running locally

### Train

```bash
uv run -m revolutionary_mlops train [--train-path data/train.csv] [--test-path data/test.csv]
```

Trains the model, evaluates it on test data, and prints the `model_id` to use for validation.

### Validate

```bash
uv run -m revolutionary_mlops validate <model_id> [--validate-path data/validate.csv]
```

Retrieves the model by `model_id` and evaluates it on validation data, printing accuracy/precision/recall.

### Data format

CSV files have no header. Each row starts with the target (`TRUE`) followed by a variable number of random features:

```
TRUE,0.4023,0.7235,0.3185
TRUE,0.1969,0.5479,0.6219,0.9172,0.2438,0.1050
```

## Testing & linting

```bash
uv run pytest tests
uv run ruff check .
uv run ruff format --check .
```
