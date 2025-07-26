from agents import Agent
from my_config.gemini_config import MODEL
from my_tools.count_scrape import get_account_total


agent2 = Agent(
    name="AMA Account Numbers Tracker Agent",
    instructions="Use only the scraping tool to get AMA account stats. Only return the numeric and word formats for h1 and h4 headings. Don't say anything else.",
    model=MODEL,
    tools=[get_account_total] 
)