from agents import Runner
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
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
    
    async def send_email(self, report: ReportData, email: str) -> None:
        input_message = f"""
        Recipient email address:
        {email}
        
        Research report:
        {report.markdown_report}
        """
        await Runner.run(email_agent,input_message)
    
