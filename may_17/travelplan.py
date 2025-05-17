# travel_planner_gemini_async.py
import os
import asyncio
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load your Google API key for Gemini
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 1) Configure the Gemini-compatible client
model_client = OpenAIChatCompletionClient(
    model="gemini-2.0-flash",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=GOOGLE_API_KEY,
)

# 2) Define each agent exactly as before
planner_agent = AssistantAgent(
    name="planner_agent",
    model_client=model_client,
    description="A helpful assistant that can plan trips.",
    system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
)

local_agent = AssistantAgent(
    name="local_agent",
    model_client=model_client,
    description="A local assistant that can suggest local activities or places to visit.",
    system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
)

language_agent = AssistantAgent(
    name="language_agent",
    model_client=model_client,
    description="A helpful assistant that can provide language tips for a given destination.",
    system_message=(
        "You are a helpful assistant that can review travel plans, providing feedback on important/critical tips "
        "about how best to address language or communication challenges for the given destination. "
        "If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale."
    ),
)

travel_summary_agent = AssistantAgent(
    name="travel_summary_agent",
    model_client=model_client,
    description="A helpful assistant that can summarize the travel plan.",
    system_message=(
        "You are a helpful assistant that can take in all of the suggestions and advice from the other agents "
        "and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. "
        "YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, "
        "you can respond with TERMINATE."
    ),
)

# 3) Build the RoundRobinGroupChat
termination = TextMentionTermination("TERMINATE")
group_chat = RoundRobinGroupChat(
    participants=[
        planner_agent,
        local_agent,
        language_agent,
        travel_summary_agent,
    ],
    termination_condition=termination,
)

# 4) Async entry point that asks for user input
async def main(task: str):
    # Stream the multi-agent discussion to the console
    await Console(group_chat.run_stream(task=task))
    # Cleanly close the model client
    await model_client.close()

if __name__ == "__main__":
    # Prompt the user for their travel-plan request
    user_task = input("Enter your travel plan request (e.g., \"Plan a 3 day trip to Nepal\"): ")
    asyncio.run(main(user_task))
