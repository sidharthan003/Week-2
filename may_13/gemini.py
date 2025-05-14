# import google.generativeai as genai

# def call_gemini(prompt):
#     genai.configure(api_key="AIzaSyDSzv8js0Z_oTWldSvI_hea2ThSGq-m8Xc")  # Replace with your key
#     model = genai.GenerativeModel("models/gemini-2.5-pro-preview-05-06")
#     response = model.generate_content(prompt)
#     return response.text

# if __name__ == "__main__":
#     prompt = "Explain the importance of chunking in LLM-based RAG pipelines."
#     output = call_gemini(prompt)
#     print("Gemini API Response:\n", output)

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key="AIzaSyDSzv8js0Z_oTWldSvI_hea2ThSGq-m8Xc",
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Explain the importance of chunking in LLM-based RAG pipelines"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()

