import os
import openai
from utils import get_datetime_str


from dotenv import load_dotenv
load_dotenv()


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# LOADING ASSETS REQUIRED BY THE PROMPT
sow_template = open("assets/sow_template.md").read()
assessment_form = open("assets/assessment_form.md").read()

# FUNCTION THAT TAKES FORM ENTRIES AS INPUT AND RETURNS GENERATED SOW
def generate_sow(data):
    prompt = f"""
    Generate a detailed Scope of Work (SOW) for the following client:
    {data}

    Use the following SOW template for reference:
    {sow_template}

    To fill "Alignment with Assessment" column, refer to the following form:
    {assessment_form}
    """

    # SAVING `prompt` FOR LOGGING
    open(f"logs/prompts/prompt_{get_datetime_str()}.txt", "w").write(prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI consultant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

