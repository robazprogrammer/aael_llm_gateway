Multi-Provider LLM Gateway

## Overview

This repository contains the source code for an experimental implementation of a multi-provider Large Language Model (LLM) gateway.

Rather than connecting an application to a single AI provider, this gateway provides a unified interface capable of routing requests to multiple AI models including OpenAI, Anthropic, Together AI, and other compatible providers.

The project was developed as part of the ongoing **AI-Augmented Exploratory Learning (AAEL)** research initiative examining how professionals learn, solve problems, and make decisions with AI.

---

## Objectives

* Demonstrate vendor-independent AI application design.
* Simplify switching between multiple LLM providers.
* Explore AI ecosystems rather than single-model workflows.
* Provide a foundation for future AAEL Labs projects.

---

## Current Providers

* OpenAI
* Anthropic
* Together AI

Additional providers can be added with minimal changes.

---

## Requirements

```bash
pip install requests
```

Set your API keys as environment variables.

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
TOGETHER_API_KEY
```

---

## Future Enhancements

* Automatic model routing
* Cost-aware provider selection
* Response quality scoring
* Prompt logging
* Experiment tracking
* Integration with AAEL workflows
* Local model support (Ollama)
* Azure OpenAI support
* Google Gemini support

---

## About AAEL

AI-Augmented Exploratory Learning (AAEL) is a learning framework centered on four iterative processes:

* Ask
* Adapt
* Evaluate
* Learn

AAEL investigates how professionals effectively collaborate with AI to solve authentic problems while developing transferable knowledge and skills.

---

## Author

Robert Foreman

Doctoral Candidate – Educational Technology
Central Michigan University

Research Focus

* AI-Augmented Exploratory Learning (AAEL)
* How Professionals Learn with AI

Website: https://NhanceData.com

---

Security Note: This project uses environment variables for API keys. Never hard-code API keys directly into the script or commit .env files to GitHub.

This repository is part of the growing AAEL Labs collection of open-source educational experiments supporting AI research, learning, and workforce development.

