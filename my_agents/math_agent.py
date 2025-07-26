from agents import Agent
from my_config.gemini_config import MODEL

agent = Agent(
    name = "Teacher",
    instructions="You are an Expert Maths Teacher, only answer the question if its related to maths. Dont answer any other question. Focused only on Maths",
    model=MODEL
)
