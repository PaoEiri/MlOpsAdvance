# revolutionary-mlops

An end-to-end **MLOps CI/CD pipeline** built on GitHub Actions — from lint to a live metrics dashboard on GitHub Pages, with zero manual steps in between.

The "model" itself is intentionally a joke (a threshold classifier that predicts `TRUE` most of the time). The point of this project isn't the ML — it's the **automation pipeline** around it: a chained sequence of workflows that lints, tests, trains, validates, and deploys on every push, complete with quality gates and historical metrics tracking.

**Live report:** https://paoeiri.github.io/MlOpsAdvance/

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
