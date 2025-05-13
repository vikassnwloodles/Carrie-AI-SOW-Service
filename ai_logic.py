import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sow(data):
    prompt = f"""
    Generate a detailed Scope of Work (SOW) for the following client:
    - Company: {data.company_name}
    - Industry: {data.industry}
    - Goals: {data.goals}
    - Current Tools: {data.current_tools}
    - Key Challenges: {data.challenges}
    - Timeline: {data.timeline}
    - Budget: {data.budget}

    The SOW should include objectives, deliverables, AI implementation plan, and next steps.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI consultant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
