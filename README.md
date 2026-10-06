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


---

## 🧠 Agent Responsibilities

The application uses multiple specialized agents, with each agent responsible for a specific part of the research workflow.

| Agent | Model | Responsibility |
|---|---|---|
| Planner Agent | DeepSeek V4 Flash | Creates a structured research plan |
| Search Agent | Gemini 3.5 Flash-Lite | Searches the web and summarizes results |
| Writer Agent | DeepSeek V4 Flash | Generates the final research report |
| Email Agent | Gemini 3.5 Flash-Lite | Formats and sends the report |

---

## 🔄 How It Works

### 1. User submits a research question

The user provides:

- Email address
- Research question

Example:

```text
What are the latest trends in AI agent development?
```

### 2. Planner Agent creates a research plan

The Planner Agent analyzes the question and generates multiple targeted search queries.

```text
Research Topic
      ↓
Planner Agent
      ↓
┌─────────────────────────────┐
│ Search 1                    │
│ Search 2                    │
│ Search 3                    │
│ Search 4                    │
└─────────────────────────────┘
```

The searches are represented using structured Pydantic models.

### 3. Search Agents perform web research

Each planned search is sent to a Search Agent.

The Search Agent uses a custom `web_search` function tool that calls the Tavily API.

The searches are executed concurrently using Python's `asyncio`.

```python
tasks = [self.search(item) for item in search_plan.searches]

return await asyncio.gather(*tasks)
```

### 4. Writer Agent generates the report

After the searches are completed, the collected research is passed to the Writer Agent.

The Writer Agent generates:

- Short summary
- Detailed Markdown report
- Follow-up questions

The structured output is validated using Pydantic.

### 5. Email Agent delivers the report

The completed report is passed to the Email Agent.

The Email Agent:

1. Receives the report and recipient email.
2. Creates an appropriate subject.
3. Converts the report into a clean HTML email.
4. Calls the email tool.
5. Sends the report to the specified recipient.

---

## ⚡ Parallel Search Execution

Independent searches are executed concurrently instead of waiting for each search to finish before starting the next one.

```text
Search 1 ───────┐
Search 2 ───────┤
Search 3 ───────┼──→ Combined Results
Search 4 ───────┘
```

This reduces unnecessary waiting during the research process.

---

## 🛠️ Tech Stack

### AI & Agents

- Python
- OpenAI Agents SDK
- Pydantic
- DeepSeek V4 Flash
- Gemini 3.5 Flash-Lite
- MixRoute

### Web Research

- Tavily Search API
- Requests

### Frontend

- Gradio
- Custom CSS
- Custom JavaScript

### Email & Notifications

- SMTP
- Gmail App Password
- Pushover

### Deployment

- GitHub
- Render

---

## 📁 Project Structure

```text
deep_research/
│
├── app.py
├── models.py
├── planner_agent.py
├── search_agent.py
├── writer_agent.py
├── email_agent.py
├── research_manager.py
├── messenger.py
├── styles.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

| File | Purpose |
|---|---|
| `app.py` | Gradio application and UI |
| `models.py` | LLM provider and model configuration |
| `planner_agent.py` | Research planning agent |
| `search_agent.py` | Web search tool and Search Agent |
| `writer_agent.py` | Final report generation |
| `email_agent.py` | Email formatting and delivery |
| `research_manager.py` | Main workflow orchestration |
| `messenger.py` | Email and Pushover functionality |
| `styles.py` | Custom UI styling and frontend configuration |

---

## 🧩 Structured Outputs

The Planner Agent uses Pydantic models to define the expected research plan.

```python
class WebSearchItem(BaseModel):
    reason: str
    query: str


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
```

The Writer Agent also returns structured output:

```python
class ReportData(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_questions: list[str]
```

Structured outputs make the different stages of the workflow easier to connect.

---

## 🔧 Function Tools

The Search Agent uses a custom function tool to access the web:

```python
@function_tool
def web_search(query: str) -> str:
    ...
```

The Email Agent uses a function tool to send the generated report:

```python
@function_tool
def send_email_tool(
    subject: str,
    text_body: str,
    html_body: str,
    recipient_email: str
) -> str:
    ...
```

---

## 🔐 Environment Variables

The application uses environment variables for API keys and credentials.

```env
MIXROUTE_API_KEY=your_mixroute_api_key
TAVILY_API_KEY=your_tavily_api_key

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_APP_PASSWORD=your_app_password

PUSHOVER_USER=your_pushover_user
PUSHOVER_TOKEN=your_pushover_token

USE_EMAIL=true
```

> **Important:** Never commit your `.env` file, API keys, passwords, or other secrets to GitHub.

---

## ⚙️ Running Locally

### Install dependencies

```bash
uv pip install -r requirements.txt
```

### Start the application

```bash
uv run app.py
```

Open:

```text
http://127.0.0.1:7860
```

---

## 🌐 Deployment

The application can be deployed using Render.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
python app.py
```

The application uses Render's dynamically assigned port:

```python
server_name="0.0.0.0"
server_port=int(os.environ.get("PORT", 7860))
```

---

## 💡 Why Multiple Models?

Instead of using one model for every task, this project uses different models for different responsibilities.

```text
Research Query
      │
      ▼
Planner Agent
DeepSeek V4 Flash
      │
      ▼
Search Agents
Gemini 3.5 Flash-Lite
      │
      ▼
Writer Agent
DeepSeek V4 Flash
      │
      ▼
Email Agent
Gemini 3.5 Flash-Lite
```

This model-routing approach helps balance:

- Cost
- Speed
- Reasoning capability
- Output quality

---

## 🎯 Key Concepts Demonstrated

- AI agents
- Multi-agent workflows
- Agent orchestration
- Function tools
- Structured outputs
- Pydantic models
- Async Python
- Parallel execution
- Web search integration
- LLM model routing
- Email automation
- Environment variable management
- Gradio application development
- Cloud deployment

---

## 📚 What I Learned

Building this project helped me move from simply calling an LLM API to designing a complete agentic workflow.

The main concepts practiced were:

- Agent orchestration
- Tool calling
- Structured outputs
- Parallel LLM calls
- Async programming
- Web search integration
- Model routing
- External API integration
- Email automation
- Deployment

---

## 🚀 Future Improvements

- [ ] Add source citations to generated reports
- [ ] Add configurable research depth
- [ ] Add PDF report generation
- [ ] Add research history
- [ ] Add downloadable reports
- [ ] Add source credibility scoring
- [ ] Add more search providers
- [ ] Add authentication
- [ ] Add persistent storage
- [ ] Add user-selectable AI models

---

## 👨‍💻 Author

### Sanket Ram

**Web Developer | Full-Stack Developer | AI Agents Learner**

Currently exploring AI agents, multi-agent systems, LLM orchestration, and AI-powered applications.

---

## ⭐ Support

If you found this project interesting, consider giving the repository a ⭐.

Feel free to explore the code and build your own version of the research agent.
