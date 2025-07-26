import streamlit as st
import asyncio
import re
from agents import Runner, set_tracing_disabled
from my_agents.scraper_agent import agent2

set_tracing_disabled(True)

st.set_page_config(page_title="AMA Accounts Tracker")
st.title("AMA Account Tracker")

st.markdown("Click the button below to get the **Total AMA Accounts** from the live site.")

async def get_result():
    return await Runner.run(
        starting_agent=agent2,
        input="Total AMA Accounts"
    )

if st.button("Get AMA Account Total"):
    with st.spinner("Scraping live data..."):
        result = asyncio.run(get_result())
        response_text = result.final_output  # plain string

        # DEBUG
        st.write("DEBUG - Raw Output:", response_text)

        # Use regex to extract values
        num_match = re.search(r"Number of Accounts:\s*([\d,]+)", response_text)
        word_match = re.search(r"Accounts in Word:\s*([\w\. ]+)", response_text)

        num_accounts = num_match.group(1) if num_match else "N/A"
        word_accounts = word_match.group(1) if word_match else "N/A"

        # Step 4: Show clean output
        # st.success("Data retrieved successfully!")
        st.subheader("Total AMA Accounts")
        st.write(f"{num_accounts}")
        st.write(f"{word_accounts}")

