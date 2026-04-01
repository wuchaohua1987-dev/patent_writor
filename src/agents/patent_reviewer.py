"""PatentReviewer agent for evaluating patent quality."""

from crewai import Agent


def create_patent_reviewer(agent_config: dict) -> Agent:
    """Create a PatentReviewer agent.

    Args:
        agent_config: Configuration dictionary from agents.yaml

    Returns:
        Configured Agent instance for patent review
    """
    return Agent(
        config=agent_config,
        verbose=True,
    )
