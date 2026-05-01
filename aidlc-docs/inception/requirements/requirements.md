# Requirements Document

## Intent Analysis

- **User Request**: Implement a GitHub Actions pipeline that executes linting and unit testing for pull requests and merges into main
- **Request Type**: Infrastructure / Developer Tooling
- **Scope**: Single configuration file (`.github/workflows/ci.yml`) + minor `pyproject.toml` update
- **Complexity**: Simple

## Functional Requirements

1. **FR-1**: A GitHub Actions workflow must be created at `.github/workflows/ci.yml`
2. **FR-2**: The workflow must trigger on:
   - Pull requests targeting the `main` branch
   - Pushes to the `main` branch (merges)
3. **FR-3**: The workflow must include a **linting** job that runs a Python linter against the source code
4. **FR-4**: The workflow must include a **unit testing** job that runs the existing `pytest` test suite
5. **FR-5**: Both jobs must run on `ubuntu-latest`
6. **FR-6**: Dependencies must be installed using the project's existing `pyproject.toml` (including dev extras)

## Non-Functional Requirements

1. **NFR-1**: Pipeline must be fast — no unnecessary caching layers beyond pip cache
2. **NFR-2**: Linting configuration must be consistent with the existing project style
3. **NFR-3**: The workflow file must be valid YAML and pass GitHub Actions schema validation

## Technical Context

- **Language**: Python (>=3.8)
- **Build System**: setuptools / pyproject.toml
- **Test Runner**: pytest
- **Existing dev deps**: pytest, pytest-mock, responses
- **Linting tool to add**: flake8 (standard, no config needed for a simple SDK)
- **Trigger events**: `pull_request` (base: main) + `push` (branch: main)
