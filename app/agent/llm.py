import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Groq OpenAI-compatible endpoint (free tier)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL_SMART = os.getenv("LLM_MODEL_SMART", "openai/gpt-oss-120b")
MODEL_FAST = os.getenv("LLM_MODEL_FAST", "openai/gpt-oss-20b")


def structured_call(system: str, user: str, schema, model: str = MODEL_SMART,
                    temperature: float = 0.3, retries: int = 3):
    """Call the LLM and return a validated pydantic object of type `schema`."""
    schema_json = json.dumps(schema.model_json_schema())
    full_system = (
        system
        + "\n\nRespond ONLY with valid JSON that matches this JSON schema:\n"
        + schema_json
    )
    last_err = None
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": full_system},
                    {"role": "user", "content": user},
                ],
            )
            return schema.model_validate_json(resp.choices[0].message.content)
        except Exception as e:  # rate limit / bad JSON -> wait and retry
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise last_err