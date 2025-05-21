import autogen
import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment variables")

# Configure Google's Gemini API
genai.configure(api_key=gemini_api_key)

class GeminiAgent(autogen.AssistantAgent):
    """Custom agent class that uses Gemini API directly"""
    
    def __init__(self, name, gemini_model="gemini-1.5-pro", **kwargs):
        super().__init__(name=name, **kwargs)
        self.gemini_model = gemini_model
        self.model = genai.GenerativeModel(gemini_model)
        
    async def _a_generate_reply(self, messages, sender, **kwargs):
        """Override the generate reply method to use Gemini API"""
        # Format the conversation history for Gemini
        formatted_messages = []
        
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            content = msg.get("content", "")
            formatted_messages.append({"role": role, "parts": [content]})
        
        try:
            # Get system message if it exists
            system_message = self.system_message if hasattr(self, "system_message") else None
            
            # Create conversation with system message if provided
            if system_message:
                convo = self.model.start_chat(history=[
                    {"role": "model", "parts": [system_message]}
                ])
            else:
                convo = self.model.start_chat()
                
            # Add all messages to the conversation
            for msg in formatted_messages:
                if msg["role"] == "user":
                    response = convo.send_message(msg["parts"][0])
            
            # Get the response
            return response.text
        except Exception as e:
            print(f"Error using Gemini API: {str(e)}")
            return f"I encountered an error when trying to generate a response: {str(e)}"

async def main():
    try:
        # Create the assistant agent using our custom GeminiAgent
        assistant = GeminiAgent(
            name="CTO",
            gemini_model="gemini-1.5-pro",
            system_message="Chief technical officer of a tech company"
        )
        
        # Create the user proxy agent with disabled Docker
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "web", "use_docker": False}
        )

        # First task
        task = """
        Write python code to output numbers 1 to 100, and then store the code in a file
        """

        print("Starting first task...")
        await user_proxy.a_initiate_chat(
            assistant,
            message=task
        )

        # Second task
        task2 = """
        Change the code in the file you just created to instead output numbers 1 to 200
        """

        print("Starting second task...")
        await user_proxy.a_initiate_chat(
            assistant,
            message=task2
        )
    
    except Exception as e:
        print(f"Error encountered: {str(e)}")
        # Print a traceback to help debug
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())