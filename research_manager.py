from agents import Runner
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
# from email_agent import email_agent
import asyncio
import markdown

class ResearchManager:

    async def run(self, query: str, email: str):
        yield "Starting research..."
        search_plan = await self.plan_searches(query)
        yield f"Searches planned, starting {len(search_plan.searches)} searches..."
        search_results = await self.perform_searches(search_plan)
        yield "Searches complete, writing report..."
        report = await self.write_report(query, search_results)
        yield "Report written, sending email..."
        await self.send_email(report, email)
        yield "Email sent, research complete"
        yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        tasks = [self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str | None:
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input_message)
        return result.final_output

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        input_message = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_message)
        return result.final_output
    
    # async def send_email(self, report: ReportData, email: str) -> None:
    #     input_message = f"""
    #     Recipient email address:
    #     {email}
        
    #     Research report:
    #     {report.markdown_report}
    #     """
    #     await Runner.run(email_agent,input_message)

    async def send_email(self, report: ReportData, email: str) -> None:
    print("EMAIL: starting email delivery")

    from messenger import send_email

    subject = "Your Deep Research Report"
    text_body = report.markdown_report

    html_report = markdown.markdown(
        report.markdown_report,
        extensions=["tables", "fenced_code"]
    )

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                color: #222;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            pre {{
                background: #f5f5f5;
                padding: 15px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Deep Research Report</h1>
        {html_report}
    </body>
    </html>
    """

    await asyncio.to_thread(
        send_email,
        subject,
        text_body,
        html_body,
        email
    )

    print("EMAIL: delivery completed")
