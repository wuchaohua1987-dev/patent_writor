"""PatentModifier agent for revising patent documents."""

from crewai import Agent


def create_patent_modifier(agent_config: dict) -> Agent:
    """Create a PatentModifier agent.

    Args:
        agent_config: Configuration dictionary from agents.yaml

    Returns:
        Configured Agent instance for patent modification
    """
    return Agent(
        config=agent_config,
        verbose=True,
    )
