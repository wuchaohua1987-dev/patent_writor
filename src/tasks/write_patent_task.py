"""Task definitions for patent writing workflow."""

from crewai import Task


def create_write_patent_task(task_config: dict) -> Task:
    """Create a patent writing task.

    Args:
        task_config: Configuration dictionary from tasks.yaml

    Returns:
        Configured Task instance for patent writing
    """
    return Task(config=task_config)


def create_search_patents_task(task_config: dict) -> Task:
    """Create a patent search task.

    Args:
        task_config: Configuration dictionary from tasks.yaml

    Returns:
        Configured Task instance for patent searching
    """
    return Task(config=task_config)


def create_review_patent_task(task_config: dict) -> Task:
    """Create a patent review task.

    Args:
        task_config: Configuration dictionary from tasks.yaml

    Returns:
        Configured Task instance for patent review
    """
    return Task(config=task_config)


def create_modify_patent_task(task_config: dict) -> Task:
    """Create a patent modification task.

    Args:
        task_config: Configuration dictionary from tasks.yaml

    Returns:
        Configured Task instance for patent modification
    """
    return Task(config=task_config)
