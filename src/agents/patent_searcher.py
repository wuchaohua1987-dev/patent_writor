"""PatentSearcher agent for searching prior art."""

from crewai import Agent
from crewai_tools import FileReadTool, DirectoryReadTool


def create_patent_searcher(agent_config: dict) -> Agent:
    """Create a PatentSearcher agent.

    Args:
        agent_config: Configuration dictionary from agents.yaml

    Returns:
        Configured Agent instance for patent searching
    """
    return Agent(
        config=agent_config,
        verbose=True,
        tools=[FileReadTool(), DirectoryReadTool()],
    )
