# import google.generativeai as genai
#
# # Google Gemini API Key
# # NOTE: It's HIGHLY recommended to load your API key from an environment variable,
# # not hardcode it in the file.
# # Example: GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
# GOOGLE_API_KEY = 'AIzaSyD9jUGPSqVRGIjCPQLwEda9YOGuM7-6yPA'
#
# # Configure the Google Gemini API
# genai.configure(api_key=GOOGLE_API_KEY)
#
# # Use a standard, currently available and recommended model.
# # 'gemini-2.5-flash' is a good, fast, and capable default.
# MODEL_NAME = 'gemini-2.5-flash'
#
# # Initialize the model once.
# try:
#     model = genai.GenerativeModel(MODEL_NAME)
#     print(f"Using model: {MODEL_NAME}")
# except Exception as e:
#     # Handle case where the model might not be found or API key is wrong
#     print(f"Error initializing model {MODEL_NAME}: {e}")
#     model = None  # Set to None if initialization fails
#
#
# # If you still want the listing logic (though usually unnecessary with a fixed name):
# # If you want to use the most powerful available *supported* model, you could do:
# # model = next((genai.GenerativeModel(m.name) for m in genai.list_models() if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name), None)
#
#
# def generate_gemini_response(prompt):
#     if not model:
#         return "Error: AI model failed to initialize."
#
#     # Add context related to career development and job-related queries
#     # NOTE: The original context prompt "This conversation focuses on book" seems
#     # to contradict the example message about "data science."
#     # Consider making it generic or removing it if not needed.
#     context_prompt = f"You are a helpful AI assistant. Respond to the following request: {prompt}"
#
#     # Generate response using the model
#     # Add a try/except for the API call in case of transient errors
#     try:
#         response = model.generate_content(context_prompt)
#         return response.text
#     except Exception as e:
#         print(f"Error generating content: {e}")
#         return "Sorry, I couldn't generate a response due to an API error."
#
#
# # Example user message related to career services
# user_message = "What are the best skills to develop for a career in data science?"
# gemini_response = generate_gemini_response(user_message)
# print(gemini_response)


import re
import google.generativeai as genai

GOOGLE_API_KEY = 'AIzaSyD9jUGPSqVRGIjCPQLwEda9YOGuM7-6yPA'
genai.configure(api_key=GOOGLE_API_KEY)

MODEL_NAME = 'gemini-2.5-flash'

try:
    model = genai.GenerativeModel(MODEL_NAME)
    print(f"Using model: {MODEL_NAME}")
except Exception as e:
    print(f"Error initializing model {MODEL_NAME}: {e}")
    model = None


def clean_text(text):
    """Remove markdown-style formatting (like **, *, and extra spaces)."""
    text = re.sub(r'\*\*', '', text)  # remove bold markers
    text = re.sub(r'\*', '', text)    # remove bullet markers
    text = re.sub(r'\s+', ' ', text)  # normalize spaces
    return text.strip()


def generate_gemini_response(prompt):
    if not model:
        return "Error: AI model failed to initialize."

    context_prompt = f"You are a helpful AI assistant. Respond clearly without markdown symbols: {prompt}"

    try:
        response = model.generate_content(context_prompt)
        clean_response = clean_text(response.text)
        return clean_response
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Sorry, I couldn't generate a response due to an API error."


# Example
user_message = "What are the best skills to develop for a career in data science?"
gemini_response = generate_gemini_response(user_message)
print(gemini_response)
