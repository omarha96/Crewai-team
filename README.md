# Crewai-team

A minimal Python project that uses [CrewAI](https://github.com/crewAIInc/crewAI) to run a **4-agent programming team**.

## Team

The project creates these agents:

1. Engineering Manager
2. Software Architect
3. Senior Developer
4. QA Engineer

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set your model provider credentials as environment variables required by CrewAI before running non-dry mode.

> Note: CrewAI dependencies are skipped on Android due to lack of upstream wheel support.
> `--dry-run` still works there, while full LLM execution should be run on a
> supported platform.

## Run

Dry run (no LLM call):

```bash
python -m crewai_team.team --dry-run
```

Run with a feature request:

```bash
python -m crewai_team.team "Build a task management API with auth and tests"
```
