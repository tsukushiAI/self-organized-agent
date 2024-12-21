import os
from openai import OpenAI
#import backoff
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

client = OpenAI(
    api_key=os.environ["OPENAI_API_SECRET_KEY"], 
    max_retries=4,
    #timeout=60,
)

#@backoff.on_exception(backoff.expo(base=2, max_value=60*5), (openai.RateLimitError, openai.OpenAIError))
#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def chat_completions(content, model, max_tokens, temperature, json_mode=False):
    if json_mode:
        response = client.chat.completions.create(
                model = model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"}
            )
    else:
        response = client.chat.completions.create(
                model = model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
    return response.choices[0].message.content


def api_chat_completions(content, json_mode=False, model_name="gpt-3.5-turbo-1106", 
                         max_tokens=1000, temperature=0.0):
    return chat_completions(content, model=model_name, max_tokens=max_tokens, 
                                temperature=temperature, json_mode=json_mode)
