import os
import openai
import re
from utils import get_datetime_str
from consts import LOGS_DIR
from prompt_components.get_prompts import get_system_prompt, get_user_prompt

import logging
logger = logging.getLogger("carrie_ai_sow_service")

from dotenv import load_dotenv
load_dotenv()


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# FUNCTION THAT TAKES FORM ENTRIES AS INPUT AND RETURNS GENERATED SOW
def generate_sow(data):
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(data)

    # SAVING `prompt` FOR LOGGING
    INPUT_LOGS_DIR = f"{LOGS_DIR}/inputs"
    os.makedirs(INPUT_LOGS_DIR, exist_ok=True)

    open(f"{INPUT_LOGS_DIR}/user_prompt_{get_datetime_str()}.txt", "w").write(user_prompt)

    logger.info("Calling OpenAI's `gpt-4o-mini` Model...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    logger.info("Processing and Returning Model Response...")
    raw_response = response.choices[0].message.content
    # SAVING `raw_response` FOR LOGGING
    OUTPUT_LOGS_DIR = f"{LOGS_DIR}/outputs"
    os.makedirs(OUTPUT_LOGS_DIR, exist_ok=True)

    open(f"{OUTPUT_LOGS_DIR}/raw_response_{get_datetime_str()}.txt", "w").write(raw_response)

    processed_response = raw_response.strip()
    
    return processed_response
