import os
from openai import OpenAI

from ..config.settings import OPENAI_API_KEY

from ..utils.resume_prompt_utils import generate_resume_prompt


def enhance_resume_content(user_input, customized_info):
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional resume optimization assistant."},
                {"role": "user", "content": generate_resume_prompt(user_input, customized_info)}
            ],
            timeout=40,
            temperature=0.7,
            max_tokens=5000
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API request failed: {str(e)}")