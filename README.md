# 🔎 Deep Research AI Agent

An AI-powered research assistant that automatically plans research, searches the web, synthesizes findings, generates a structured report, and delivers the final report directly to your email.

Built using the **OpenAI Agents SDK**, multiple LLM providers, Tavily Web Search, and a Gradio interface.

---

## 🚀 Live Demo

🔗 **Live App:** https://deep-research-agent-ucm4.onrender.com

---

## ✨ Features

- 🧠 **AI Research Planning**
  - Breaks a research question into multiple targeted web searches.
  - Uses a dedicated Planner Agent to determine what information is needed.

- 🔎 **Parallel Web Research**
  - Performs multiple searches concurrently.
  - Uses Tavily to retrieve relevant web results.
  - Each search is handled by a dedicated Search Agent.

- 📝 **AI Report Generation**
  - Combines the collected research into a comprehensive report.
  - Generates:
    - Short summary
    - Detailed Markdown report
    - Suggested follow-up questions

- 📧 **Automatic Email Delivery**
  - Sends the completed research report directly to the user's email.
  - Generates a clean HTML email automatically.

- 🔔 **Pushover Fallback**
  - Supports Pushover notifications when email delivery is disabled.

- ⚡ **Multi-Model Architecture**
  - Different agents use different LLMs depending on the task.
  - Optimized for cost and performance.

- 🎨 **Custom Gradio UI**
  - Clean research interface.
  - Custom CSS styling.
  - Example research questions.
  - Live progress updates.

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      User Query     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Planner Agent    │
                         │  DeepSeek V4 Flash  │
                         └──────────┬──────────┘
                                    │
                              Search Plan
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │  Search Agent  │ │  Search Agent  │ │  Search Agent  │
        │ Gemini Flash   │ │ Gemini Flash   │ │ Gemini Flash   │
        │     Lite       │ │     Lite       │ │     Lite       │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │     Writer Agent    │
                         │  DeepSeek V4 Flash  │
                         └──────────┬──────────┘
                                    │
                              Final Report
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Email Agent     │
                         │ Gemini Flash-Lite   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                              📧 Email
