<p align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/hero/wordmark-dark.svg">
        <img alt="DeepEval." src="assets/hero/wordmark-light.svg" width="520">
    </picture>
</p>

<p align="center">
    <h1 align="center">The LLM Evaluation Framework</h1>
</p>

<p align="center">
<a href="https://trendshift.io/repositories/5917" target="_blank"><img src="https://trendshift.io/api/badge/repositories/5917" alt="confident-ai%2Fdeepeval | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

<p align="center">
    <a href="https://discord.gg/3SEyvpgu2f">
        <img alt="discord-invite" src="https://dcbadge.limes.pink/api/server/3SEyvpgu2f?style=flat">
    </a>
    <a href="https://www.reddit.com/r/deepeval/">
        <img alt="reddit-community" src="https://img.shields.io/badge/Reddit-r%2Fdeepeval-FF4500?logo=reddit&logoColor=white">
    </a>
</p>

<h4 align="center">
    <p>
        <a href="https://deepeval.com/docs/getting-started?utm_source=GitHub">Documentation</a> |
        <a href="#-metrics-and-features">Metrics and Features</a> |
        <a href="#-quickstart">Getting Started</a> |
        <a href="#-integrations">Integrations</a> |
        <a href="https://www.confident-ai.com?utm_source=deepeval&utm_medium=github&utm_content=header_nav&ref_page=github/readme">Confident AI</a>
    <p>
</h4>

<p align="center">
    <a href="https://github.com/confident-ai/deepeval/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/confident-ai/deepeval.svg?color=violet">
    </a>
    <a href="https://colab.research.google.com/drive/1PPxYEBa6eu__LquGoFFJZkhYgWVYE6kh?usp=sharing">
        <img alt="Try Quickstart in Colab" src="https://colab.research.google.com/assets/colab-badge.svg">
    </a>
    <a href="https://github.com/confident-ai/deepeval/blob/master/LICENSE.md">
        <img alt="License" src="https://img.shields.io/github/license/confident-ai/deepeval.svg?color=yellow">
    </a>
    <a href="https://x.com/deepeval">
        <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/deepeval?style=social&logo=x">
    </a>
</p>

<p align="center">
    <!-- Keep these links. Translations will automatically update with the README. -->
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=de">Deutsch</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=es">Español</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=fr">français</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=ja">日本語</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=ko">한국어</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=pt">Português</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=ru">Русский</a> | 
    <a href="https://www.readme-i18n.com/confident-ai/deepeval?lang=zh">中文</a>
</p>

**DeepEval** is a simple-to-use, open-source LLM evaluation framework, for evaluating large-language model systems. It is similar to Pytest but specialized for unit testing LLM apps. DeepEval incorporates the latest research to run evals via metrics such as G-Eval, task completion, answer relevancy, hallucination, etc., which use LLM-as-a-judge and other NLP models that run **locally on your machine**.

Whether you're building AI agents, RAG pipelines, or chatbots, implemented via LangChain or OpenAI, DeepEval has you covered. With it, you can easily evaluate:

- **LLM apps end-to-end** as black boxes
- **Complete agent trajectories** across every decision and action
- **Individual agent steps** such as LLM calls, tool use, retrieval, and sub-agent handoffs

Use these evaluations to determine the optimal models, prompts, and architecture to improve your AI quality, prevent prompt drifting, or even transition from OpenAI to Claude with confidence.

> Jev is now available in DeepEval, both in existing metrics and the latest [JevEval.](https://deepeval.com/docs/metrics-jev-eval)

> [!IMPORTANT]
> If you're already in production, [Confident AI](https://www.confident-ai.com?utm_source=deepeval&utm_medium=github&utm_content=signup_callout&ref_page=github/readme) surfaces failing traces before anyone has written an eval for them, clusters them into failure modes, and turns them into your next eval.
>
> ![Demo GIF](assets/demo.gif)

<br />

# 🔥 Metrics and Features

- 📐 Large variety of ready-to-use LLM eval metrics (all with explanations) powered by **ANY** LLM of your choice, statistical methods, or NLP models that run **locally on your machine** covering all use cases:

  - **Custom, All-Purpose Metrics:**

    - [JevEval](https://deepeval.com/docs/metrics-jev-eval) — a custom metric scored by Jev, a System One model that answers your questions with calibrated probabilities instead of generated text
    - [G-Eval](https://deepeval.com/docs/metrics-llm-evals) — a research-backed LLM-as-a-judge metric for evaluating on any custom criteria with human-like accuracy
    - [DAG](https://deepeval.com/docs/metrics-dag) — DeepEval's graph-based deterministic LLM-as-a-judge metric builder

  - <details>
    <summary><b>Agentic Metrics</b></summary>

    - [Task Completion](https://deepeval.com/docs/metrics-task-completion) — evaluate whether an agent accomplished its goal
    - [Tool Correctness](https://deepeval.com/docs/metrics-tool-correctness) — check if the right tools were called with the right arguments
    - [Goal Accuracy](https://deepeval.com/docs/metrics-goal-accuracy) — measure how accurately the agent achieved the intended goal
    - [Step Efficiency](https://deepeval.com/docs/metrics-step-efficiency) — evaluate whether the agent took unnecessary steps
    - [Plan Adherence](https://deepeval.com/docs/metrics-plan-adherence) — check if the agent followed the expected plan
    - [Plan Quality](https://deepeval.com/docs/metrics-plan-quality) — evaluate the quality of the agent's plan
    - [Tool Use](https://deepeval.com/docs/metrics-tool-use) — measure quality of tool usage
    - [Argument Correctness](https://deepeval.com/docs/metrics-argument-correctness) — validate tool call arguments

    </details>

  - <details>
    <summary><b>RAG Metrics</b></summary>

    - [Answer Relevancy](https://deepeval.com/docs/metrics-answer-relevancy) — measure how relevant the RAG pipeline's output is to the input
    - [Faithfulness](https://deepeval.com/docs/metrics-faithfulness) — evaluate whether the RAG pipeline's output factually aligns with the retrieval context
    - [Contextual Recall](https://deepeval.com/docs/metrics-contextual-recall) — measure how well the RAG pipeline's retrieval context aligns with the expected output
    - [Contextual Precision](https://deepeval.com/docs/metrics-contextual-precision) — evaluate whether relevant nodes in the RAG pipeline's retrieval context are ranked higher
    - [Contextual Relevancy](https://deepeval.com/docs/metrics-contextual-relevancy) — measure the overall relevance of the RAG pipeline's retrieval context to the input
    - [RAGAS](https://deepeval.com/docs/metrics-ragas) — average of answer relevancy, faithfulness, contextual precision, and contextual recall

    </details>

  - <details>
    <summary><b>Multi-Turn Metrics</b></summary>

    - [Knowledge Retention](https://deepeval.com/docs/metrics-knowledge-retention) — evaluate whether the chatbot retains factual information throughout a conversation
    - [Conversation Completeness](https://deepeval.com/docs/metrics-conversation-completeness) — measure whether the chatbot satisfies user needs throughout a conversation
    - [Turn Relevancy](https://deepeval.com/docs/metrics-turn-relevancy) — evaluate whether the chatbot generates consistently relevant responses throughout a conversation
    - [Turn Faithfulness](https://deepeval.com/docs/metrics-turn-faithfulness) — check if the chatbot's responses are factually grounded in retrieval context across turns
    - [Role Adherence](https://deepeval.com/docs/metrics-role-adherence) — evaluate whether the chatbot adheres to its assigned role throughout a conversation

    </details>

  - <details>
    <summary><b>MCP Metrics</b></summary>

    - [MCP Task Completion](https://deepeval.com/docs/metrics-mcp-task-completion) — evaluate how effectively an MCP-based agent accomplishes a task
    - [MCP Use](https://deepeval.com/docs/metrics-mcp-use) — measure how effectively an agent uses its available MCP servers
    - [Multi-Turn MCP Use](https://deepeval.com/docs/metrics-multi-turn-mcp-use) — evaluate MCP server usage across conversation turns

    </details>

  - <details>
    <summary><b>Multimodal Metrics</b></summary>

    - [Text to Image](https://deepeval.com/docs/multimodal-metrics-text-to-image) — evaluate image generation quality based on semantic consistency and perceptual quality
    - [Image Editing](https://deepeval.com/docs/multimodal-metrics-image-editing) — evaluate image editing quality based on semantic consistency and perceptual quality
    - [Image Coherence](https://deepeval.com/docs/multimodal-metrics-image-coherence) — measure how well images align with their accompanying text
    - [Image Helpfulness](https://deepeval.com/docs/multimodal-metrics-image-helpfulness) — evaluate how effectively images contribute to user comprehension of the text
    - [Image Reference](https://deepeval.com/docs/multimodal-metrics-image-reference) — evaluate how accurately images are referred to or explained by accompanying text

    </details>

  - <details>
    <summary><b>Other Metrics</b></summary>

    - [Hallucination](https://deepeval.com/docs/metrics-hallucination) — check whether the LLM generates factually correct information against provided context
    - [Summarization](https://deepeval.com/docs/metrics-summarization) — evaluate whether summaries are factually correct and include necessary details
    - [Bias](https://deepeval.com/docs/metrics-bias) — detect gender, racial, or political bias in LLM outputs
    - [Toxicity](https://deepeval.com/docs/metrics-toxicity) — evaluate toxicity in LLM outputs
    - [JSON Correctness](https://deepeval.com/docs/metrics-json-correctness) — check whether the output matches an expected JSON schema
    - [Prompt Alignment](https://deepeval.com/docs/metrics-prompt-alignment) — measure whether the output aligns with instructions in the prompt template

    </details>

- 🎯 Supports both end-to-end and component-level LLM evaluation.
- 🧩 Build your own custom metrics that are automatically integrated with DeepEval's ecosystem.
- 🔮 Generate both single and multi-turn synthetic datasets for evaluation.
- 🔗 Integrates seamlessly with **ANY** CI/CD environment.
- 🧬 Optimize prompts automatically based on evaluation results.
- 🏆 Easily benchmark **ANY** LLM on popular LLM benchmarks in [under 10 lines of code.](https://deepeval.com/docs/benchmarks-introduction?utm_source=GitHub), including MMLU, HellaSwag, DROP, BIG-Bench Hard, TruthfulQA, HumanEval, GSM8K.

<br />

# 🔌 Integrations

DeepEval plugs into any LLM framework — OpenAI Agents, LangChain, CrewAI, and more. The same traces can go to **Confident AI** once you're live, where evals run on every production trace.

## Frameworks

- [LangChain](https://www.deepeval.com/integrations/frameworks/langchain?utm_source=GitHub) — evaluate LangChain applications with a callback handler
- [LangGraph](https://www.deepeval.com/integrations/frameworks/langgraph?utm_source=GitHub) — evaluate LangGraph agents with a callback handler
- [Pydantic AI](https://www.deepeval.com/integrations/frameworks/pydanticai?utm_source=GitHub) — evaluate Pydantic AI agents with type-safe validation
- [CrewAI](https://www.deepeval.com/integrations/frameworks/crewai?utm_source=GitHub) — evaluate CrewAI multi-agent systems
- [Anthropic](https://www.deepeval.com/integrations/frameworks/anthropic?utm_source=GitHub) — evaluate and trace Claude applications via a