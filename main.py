from agents import Runner, set_tracing_disabled
from my_agents.math_agent import agent
from my_agents.scraper_agent import agent2

set_tracing_disabled(True)

# user_input = input("Enter your Maths question here: ")

result = Runner.run_sync(
    starting_agent=agent2,
    input="Total AMA Accounts")

print(result.final_output)