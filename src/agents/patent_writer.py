"""PatentWriter agent for drafting patent documents."""

from crewai import Agent


def create_patent_writer(agent_config: dict) -> Agent:
    """Create a PatentWriter agent.

    Args:
        agent_config: Configuration dictionary from agents.yaml

    Returns:
        Configured Agent instance for patent writing
    """
    return Agent(
        config=agent_config,
        verbose=True,
    )
