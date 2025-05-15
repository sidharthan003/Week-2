import os
import dotenv
import google.generativeai as genai

# Load environment variables from .env file
dotenv.load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    # Fallback to hardcoded key if environment variable is not set
    API_KEY = "AIzaSyDSzv8js0Z_oTWldSvI_hea2ThSGq-m8Xc"  # Replace with your actual API key

# Configure Gemini API
genai.configure(api_key=API_KEY)

def generate_answer(context: str, question: str) -> str:
    prompt = (
        f"You are an expert assistant. Use the following context to answer the question.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"