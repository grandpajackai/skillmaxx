# Atomic Agents

<img src="./.assets/logo.png" alt="Atomic Agents" width="350"/>

[![PyPI version](https://badge.fury.io/py/atomic-agents.svg)](https://badge.fury.io/py/atomic-agents)
[![Documentation](https://img.shields.io/badge/docs-read%20the%20docs-blue?logo=readthedocs&style=flat-square)](https://eigenwise.github.io/atomic-agents/)
[![Build Docs](https://github.com/eigenwise/atomic-agents/actions/workflows/docs.yml/badge.svg)](https://github.com/eigenwise/atomic-agents/actions/workflows/docs.yml)
[![Code Quality](https://github.com/eigenwise/atomic-agents/actions/workflows/code-quality.yml/badge.svg)](https://github.com/eigenwise/atomic-agents/actions/workflows/code-quality.yml)
[![Discord](https://img.shields.io/badge/chat-on%20discord-7289DA?logo=discord&style=flat-square)](https://discord.gg/J3W9b5AZJR)
[![PyPI downloads](https://img.shields.io/pypi/dm/atomic-agents?style=flat-square)](https://pypi.org/project/atomic-agents/)
[![Python Versions](https://img.shields.io/pypi/pyversions/atomic-agents?style=flat-square)](https://pypi.org/project/atomic-agents/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/eigenwise/atomic-agents?style=social)](https://github.com/eigenwise/atomic-agents/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/eigenwise/atomic-agents?style=social)](https://github.com/eigenwise/atomic-agents/network/members)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/eigenwise/atomic-agents)

## What is Atomic Agents?

The Atomic Agents framework is designed around the concept of atomicity to be an extremely lightweight and modular framework for building Agentic AI pipelines and applications without sacrificing developer experience and maintainability.

Think of it like building AI applications with LEGO blocks - each component (agent, tool, context provider) is:
- **Single-purpose**: Does one thing well
- **Reusable**: Can be used in multiple pipelines
- **Composable**: Easily combines with other components
- **Predictable**: Produces consistent, reliable outputs

Built on [Instructor](https://github.com/jxnl/instructor) and [Pydantic](https://docs.pydantic.dev/latest/), it enables you to create AI applications with the same software engineering principles you already know and love.

**NEW: Join our community on Discord at [discord.gg/J3W9b5AZJR](https://discord.gg/J3W9b5AZJR) and our official subreddit at [/r/AtomicAgents](https://www.reddit.com/r/AtomicAgents/)!**

## Table of Contents

- [Atomic Agents](#atomic-agents)
  - [What is Atomic Agents?](#what-is-atomic-agents)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Quick Example](#quick-example)
  - [Why Atomic Agents?](#why-atomic-agents)
  - [Core Concepts](#core-concepts)
    - [Anatomy of an Agent](#anatomy-of-an-agent)
    - [Context Providers](#context-providers)
    - [Chaining Schemas and Agents](#chaining-schemas-and-agents)
  - [Examples \& Documentation](#examples--documentation)
    - [Quickstart Examples](#quickstart-examples)
    - [Complete Examples](#complete-examples)
  - [AI-Assisted Development](#ai-assisted-development)
    - [Project instructions (Cursor, Windsurf, Cline, Continue, and Aider)](#project-instructions-cursor-windsurf-cline-continue-and-aider)
    - [Agent skills (Claude Code, Cursor, Copilot, Codex, Windsurf, Gemini CLI, ...)](#agent-skills-claude-code-cursor-copilot-codex-windsurf-gemini-cli-)
    - [Docs for LLMs](#docs-for-llms)
  - [🚀 Version 2.0 Released!](#-version-20-released)
    - [Key Changes in v2.0:](#key-changes-in-v20)
    - [⚠️ Upgrading from v1.x](#️-upgrading-from-v1x)
  - [Atomic Forge \& CLI](#atomic-forge--cli)
    - [Running the CLI](#running-the-cli)
  - [Project Structure](#project-structure)
  - [Provider \& Model Compatibility](#provider--model-compatibility)
  - [Support](#support)
  - [Contributing](#contributing)
  - [License](#license)
  - [Additional Resources](#additional-resources)
  - [Star History](#star-history)

## Getting Started

### Installation
To install Atomic Agents, you can use pip:

```bash
pip install atomic-agents
```

Make sure you also install the provider you want to use. Provider SDKs are available as instructor extras:

```bash
pip install instructor[groq]        # for Groq
pip install instructor[anthropic]   # for Anthropic
pip install instructor[google-genai] # for Gemini
```

OpenAI is included by default. For a full list of supported providers, see the [Instructor docs](https://python.useinstructor.com/integrations/).

This also installs the CLI *Atomic Assembler*, which can be used to download Tools (and soon also Agents and Pipelines).

### Quick Example

Here's a quick snippet demonstrating how easy it is to create a powerful agent with Atomic Agents:

```python
from pydantic import Field
from openai import OpenAI
import instructor
from atomic_agents import AtomicAgent, AgentConfig, BasicChatInputSchema, BaseIOSchema
from atomic_agents.context import SystemPromptGenerator, ChatHistory

# Define a custom output schema
class CustomOutputSchema(BaseIOSchema):
    """
    docstring for the custom output schema
    """
    chat_message: str = Field(..., description="The chat message from the agent.")
    suggested_questions: list[str] = Field(..., description="Suggested follow-up questions.")

# Set up the system prompt
system_prompt_generator = SystemPromptGenerator(
    background=["This assistant is knowledgeable, helpful, and suggests follow-up questions."],
    steps=[
        "Analyze the user's input to understand the context and intent.",
        "Formulate a relevant and informative response.",
        "Generate 3 suggested follow-up questions for the user."
    ],
    output_instructions=[
        "Provide clear and concise information in response to user queries.",
        "Conclude each response with 3 relevant suggested questions for the user."
    ]
)

# Initialize OpenAI client
client = instructor.from_openai(OpenAI())

# Initialize the agent
agent = AtomicAgent[BasicChatInputSchema, CustomOutputSchema](
    config=AgentConfig(
        client=client,
        model="gpt-5-mini",
        system_prompt_generator=system_prompt_generator,
        history=ChatHistory(),
    )
)

# Example usage
if __name__ == "__main__":
    user_input = "Tell me about atomic agents framework"
    response = agent.run(BasicChatInputSchema(chat_message=user_input))
    print(f"Agent: {response.chat_message}")
    print("Suggested questions:")
    for question in response.suggested_questions:
        print(f"- {question}")
```

## Why Atomic Agents?
While existing frameworks for agentic AI focus on building autonomous multi-agent systems, they often lack the control and predictability required for real-world applications. Businesses need AI systems that produce consistent, reliable outputs aligned with their brand and objectives.

Atomic Agents addresses this need by providing:

- **Modularity:** Build AI applications by combining small, reusable components.
- **Predictability:** Define clear input and output schemas to ensure consistent behavior.
- **Extensibility:** Easily swap out components or integrate new ones without disrupting the entire system.
- **Control:** Fine-tune each part of the system individually, from system prompts to tool integrations.

All logic and control flows are written in Python, enabling developers to apply familiar best practices and workflows from traditional software development without compromising flexibility or clarity.

## Core Concepts

### Anatomy of an Agent
In Atomic Agents, an agent is composed of several key components:

- **System Prompt:** Defines the agent's behavior and purpose.
- **Input Schema:** Specifies the structure and validation rules for the agent's input.
- **Output Schema:** Specifies the structure and validation rules for the agent's output.
- **History:** Stores conversation history or other relevant data.
- **Context Providers:** Inject dynamic context into the agent's system prompt at runtime.

Here's a high-level architecture diagram:
<!-- ![alt text](./.assets/architecture_highlevel_overview.png) -->
<img src="./.assets/architecture_highlevel_overview.png" alt="High-level architecture overview of Atomic Agents" width="600"/>
<img src="./.assets/what_is_sent_in_prompt.png" alt="Diagram showing what is sent to the LLM in the prompt" width="600"/>

### Context Providers

Atomic Agents allows you to enhance your agents with dynamic context using **Context Providers**. Context Providers enable you to inject additional information into the agent's system prompt at runtime, making your agents more flexible and context-aware.

To use a Context Provider, create a class that inherits from `BaseDynamicContextProvider` and implements the `get_info()` method, which returns the context string to be added to the system prompt.

Here's a simple example:

```python
from atomic_agents.context import BaseDynamicContextProvider

class SearchResultsProvider(BaseDynamicContextProvider):
    def __init__(self, title: str, search_results: List[str]):
        super().__init__(title=title)
        self.search_results = search_results

    def get_info(self) -> str:
        return "\n".join(self.search_results)
```

You can then register your Context Provider with the agent:

```python
# Initialize your context provider with dynamic data
search_results_provider = SearchResultsProvider(
    title="Search Results",
    search_results=["Result 1", "Result 2", "Result 3"]
)

# Register the context provider with the agent
agent.register_context_provider("search_results", search_results_provider)
```

This allows your agent to include the search results (or any other context) in its system prompt, enhancing its responses based on the latest information.

### Chaining Schemas and Agents

Atomic Agents makes it easy to chain agents and tools together by aligning their input and output schemas. This design allows you to swap out components effortlessly, promoting modularity and reusability in your AI applications.

Suppose you have an agent that generates search queries and you want to use these queries with different search tools. By aligning the agent's output schema with the input schema of the search tool, you can easily chain them together or switch between different search providers.

Here's how you can achieve this:

```python
import instructor
import openai
from pydantic import Field
from atomic_agents import BaseIOSchema, AtomicAgent, AgentConfig
from atomic_agents.context import SystemPromptGenerator

# Import the search tool you want to use
from web_search_agent.tools.searxng_search import SearXNGSearchTool

# Define the input schema for the query agent
class QueryAgentInputSchema(BaseIOSchema):
    """Input schema for the QueryAgent."""
    instruction: str = Field(..., description="Instruction to generate search queries for.")
    num_queries: int = Field(..., description="Number of queries to generate.")

# Initialize the query agent
query_agent = AtomicAgent[QueryAgentInputSchema, SearXNGSearchTool.input_schema](
    config=AgentConfig(
        client=instructor.from_openai(openai.OpenAI()),
        model="gpt-5-mini",
        system_prompt_generator=SystemPromptGenerator(
            background=[
                "You are an intelligent query generation expert.",
                "Your task is to generate a specified number of diverse and highly relevant queries based on a given instruction."
            ],
            steps=[
                "Receive the instruction and the number of queries to generate.",
                "Generate the queries in JSON format."
            ],
            output_instructions=[
                "Ensure each query is unique and relevant.",
                "Provide the queries in the expected schema."
            ],
        ),
    )
)
