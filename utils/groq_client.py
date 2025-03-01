import os
from dotenv import load_dotenv

load_dotenv()
from groq import Groq

def get_groq_response(prompt: str) -> str:
    """
    Get response from Groq API for network troubleshooting
    """
    try:
        # Initialize Groq client
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        
        # Prepare system message for network troubleshooting context
        system_message = """You are a network troubleshooting expert. 
        Provide clear, step-by-step solutions for network-related issues. 
        Focus on practical advice and best practices."""
        
        # Get completion from Groq
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: Unable to get response from Groq API. {str(e)}"
