"""Patent crew orchestration for multi-agent patent writing workflow."""

from pathlib import Path
from typing import Any

import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.agents import (
    create_patent_writer,
    create_patent_searcher,
    create_patent_reviewer,
    create_patent_modifier,
)
from src.tasks import (
    create_write_patent_task,
    create_search_patents_task,
    create_review_patent_task,
    create_modify_patent_task,
)


def _load_yaml_config(file_path: Path) -> dict[str, Any]:
    """Load YAML configuration file.

    Args:
        file_path: Path to the YAML file

    Returns:
        Dictionary containing the YAML configuration
    """
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config if config else {}


@CrewBase
class PatentCrew:
    """Patent writing crew that orchestrates agents and tasks.

    This crew implements a sequential workflow:
    1. PatentWriter drafts the initial patent
    2. PatentSearcher finds relevant prior art
    3. PatentReviewer evaluates the patent quality
    4. PatentModifier refines based on feedback
    """

    def __init__(self, config_dir: Path | None = None):
        """Initialize the PatentCrew.

        Args:
            config_dir: Directory containing agents.yaml and tasks.yaml.
                       Defaults to src/config/
        """
        if config_dir is None:
            config_dir = Path(__file__).parent.parent / "config"

        self._agents_config = _load_yaml_config(config_dir / "agents.yaml")
        self._tasks_config = _load_yaml_config(config_dir / "tasks.yaml")

        # Store agent instances
        self._writer: Agent | None = None
        self._searcher: Agent | None = None
        self._reviewer: Agent | None = None
        self._modifier: Agent | None = None

        # Store task instances
        self._write_task: Task | None = None
        self._search_task: Task | None = None
        self._review_task: Task | None = None
        self._modify_task: Task | None = None

    @property
    def agents_config(self) -> dict[str, Any]:
        """Get agents configuration."""
        return self._agents_config

    @property
    def tasks_config(self) -> dict[str, Any]:
        """Get tasks configuration."""
        return self._tasks_config

    @agent
    def patent_writer(self) -> Agent:
        """Create the PatentWriter agent."""
        if self._writer is None:
            self._writer = create_patent_writer(self.agents_config["patent_writer"])
        return self._writer

    @agent
    def patent_searcher(self) -> Agent:
        """Create the PatentSearcher agent."""
        if self._searcher is None:
            self._searcher = create_patent_searcher(
                self.agents_config["patent_searcher"]
            )
        return self._searcher

    @agent
    def patent_reviewer(self) -> Agent:
        """Create the PatentReviewer agent."""
        if self._reviewer is None:
            self._reviewer = create_patent_reviewer(
                self.agents_config["patent_reviewer"]
            )
        return self._reviewer

    @agent
    def patent_modifier(self) -> Agent:
        """Create the PatentModifier agent."""
        if self._modifier is None:
            self._modifier = create_patent_modifier(
                self.agents_config["patent_modifier"]
            )
        return self._modifier

    @task
    def write_patent_task(self) -> Task:
        """Create the patent writing task."""
        if self._write_task is None:
            self._write_task = create_write_patent_task(
                self.tasks_config["write_patent"]
            )
            self._write_task.agent = self.patent_writer()
        return self._write_task

    @task
    def search_patents_task(self) -> Task:
        """Create the patent search task."""
        if self._search_task is None:
            self._search_task = create_search_patents_task(
                self.tasks_config["search_patents"]
            )
            self._search_task.agent = self.patent_searcher()
        return self._search_task

    @task
    def review_patent_task(self) -> Task:
        """Create the patent review task."""
        if self._review_task is None:
            self._review_task = create_review_patent_task(
                self.tasks_config["review_patent"]
            )
            self._review_task.agent = self.patent_reviewer()
        return self._review_task

    @task
    def modify_patent_task(self) -> Task:
        """Create the patent modification task."""
        if self._modify_task is None:
            self._modify_task = create_modify_patent_task(
                self.tasks_config["modify_patent"]
            )
            self._modify_task.agent = self.patent_modifier()
        return self._modify_task

    @crew
    def crew(self) -> Crew:
        """Create the patent writing crew."""
        return Crew(
            agents=[
                self.patent_writer(),
                self.patent_searcher(),
                self.patent_reviewer(),
                self.patent_modifier(),
            ],
            tasks=[
                self.write_patent_task(),
                self.search_patents_task(),
                self.review_patent_task(),
                self.modify_patent_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )

    def run(self, inputs: dict[str, Any]) -> Any:
        """Run the patent writing workflow.

        Args:
            inputs: Dictionary containing input data for the workflow
                    Expected keys:
                    - input_file: Path to the input markdown file
                    - search_directory: Path to directory for prior art search
                    - output_file: Path for the final patent output

        Returns:
            The result of the crew execution
        """
        return self.crew().kickoff(inputs=inputs)
