from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from crewai import Crew


AGENT_ROLES = [
    "Engineering Manager",
    "Software Architect",
    "Senior Developer",
    "QA Engineer",
]


def create_programming_crew() -> Crew:
    from crewai import Agent, Crew, Process, Task

    planner = Agent(
        role="Engineering Manager",
        goal="Plan a reliable implementation roadmap for the requested feature",
        backstory="You coordinate delivery with clear milestones and constraints.",
    )

    architect = Agent(
        role="Software Architect",
        goal="Design an implementation that is maintainable and scalable",
        backstory="You turn requirements into practical architecture decisions.",
    )

    developer = Agent(
        role="Senior Developer",
        goal="Produce clean implementation details and code-level steps",
        backstory="You focus on writing practical, testable implementation plans.",
    )

    qa = Agent(
        role="QA Engineer",
        goal="Validate acceptance criteria, test strategy, and risk coverage",
        backstory="You identify edge cases and define focused verification steps.",
    )

    tasks = [
        Task(
            description=(
                "Analyze the feature request: {feature_request}. "
                "Break down scope, assumptions, and delivery phases."
            ),
            expected_output="A prioritized implementation plan with milestones.",
            agent=planner,
        ),
        Task(
            description=(
                "Using the plan, propose architecture choices, data flow, and interfaces."
            ),
            expected_output="A concise architecture proposal with trade-offs.",
            agent=architect,
        ),
        Task(
            description=(
                "Convert the architecture into implementation steps and pseudo-code-level detail."
            ),
            expected_output="Actionable coding steps and module breakdown.",
            agent=developer,
        ),
        Task(
            description=(
                "Review the proposed implementation and define a test strategy, "
                "including edge cases and acceptance checks."
            ),
            expected_output="A test plan with acceptance criteria and risks.",
            agent=qa,
        ),
    ]

    return Crew(
        agents=[planner, architect, developer, qa],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a 4-agent CrewAI programming team"
    )
    parser.add_argument(
        "feature_request",
        nargs="?",
        default="Create a small Python API with authentication and tests",
        help="Feature request for the programming team",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print team setup only, without calling an LLM",
    )

    args = parser.parse_args()

    if args.dry_run:
        print("Programming team initialized with agents:")
        for role in AGENT_ROLES:
            print(f"- {role}")
        return

    try:
        crew = create_programming_crew()
    except ModuleNotFoundError as exc:
        if exc.name and exc.name.split(".")[0] == "crewai":
            raise SystemExit(
                "CrewAI is required for non-dry runs. Install dependencies on a "
                "supported platform, then retry."
            ) from exc
        raise

    result = crew.kickoff(inputs={"feature_request": args.feature_request})
    print(result)


if __name__ == "__main__":
    main()
