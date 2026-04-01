# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Patent Writor is a multi-agent system for patent writing and analysis using the crewAI framework. The system consists of multiple specialized agents that work together to:

1. **Patent Writing (专利写作)**: Generate patent drafts from markdown input documents
2. **Patent Search (专利检索)**: Search patents via Google Scholar (MCP/websearch tools) or read from local file directories
3. **Patent Review (专利评审)**: Evaluate patent drafts across four dimensions:
   - Innovation (创新点)
   - Value (价值)
   - Avoidability (可规避性)
   - Detectability (可检测性)
4. **Patent Modification (专利修改)**: Update patent drafts based on search results and reviews
5. **Document Conversion (文档格式转换)**: Convert between docx and markdown formats

## Technology Stack

- **Framework**: crewAI (multi-agent orchestration)
- **Language**: Python 3.12+
- **Package Manager**: uv (uses pyproject.toml)
- **External Tools**: MCP servers, websearch, Google Scholar API

## Commands

```bash
# Install dependencies
uv sync

# Add a dependency
uv add <package-name>

# Add dev dependency
uv add --dev <package-name>

# Run main application
uv run python main.py

# Run tests (when tests exist)
uv run pytest

# Run specific test
uv run pytest tests/test_file.py::test_name -v

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
uv run ruff format src/
```

## Architecture

The system follows crewAI's agent-based architecture:

```
patent_writor/
├── src/
│   ├── agents/          # Agent definitions (writer, searcher, reviewer, modifier)
│   ├── tasks/           # Task definitions for each agent
│   ├── tools/           # Custom tools (search, document conversion, etc.)
│   ├── crews/           # Crew orchestrations combining agents and tasks
│   └── utils/           # Shared utilities
├── tests/               # Test files
├── main.py              # Entry point
└── pyproject.toml       # Project configuration
```

### Agent Roles

| Agent | Role | Tools Used |
|-------|------|------------|
| PatentWriter | Draft patent documents from input | Document tools |
| PatentSearcher | Search existing patents | MCP, websearch, file reader |
| PatentReviewer | Evaluate patent quality | Analysis tools |
| PatentModifier | Revise patents based on feedback | Document tools |

### Data Flow

```
Input (markdown) → PatentWriter → Draft
                                      ↓
Draft + Search Query → PatentSearcher → Prior Art
                                              ↓
Draft + Prior Art → PatentReviewer → Review Report
                                              ↓
Draft + Review → PatentModifier → Final Patent
```

## crewAI Conventions

- Define agents in `src/agents/` with clear role, goal, and backstory
- Define tasks in `src/tasks/` with expected input/output
- Define tools in `src/tools/` as crewAI Tool classes
- Crews orchestrate agents and tasks in `src/crews/`
- Use type hints for all function parameters and returns

## MCP Integration

When adding MCP tools for patent search:
1. Configure MCP server in crewAI tool definitions
2. Handle rate limiting for external APIs
3. Cache results to minimize API calls
4. Support both online (Google Scholar) and offline (local files) search modes

## External Resources

- **crewAI Repository**: https://github.com/crewAIInc/crewAI
- **crewAI Documentation**: https://docs.crewai.com/
