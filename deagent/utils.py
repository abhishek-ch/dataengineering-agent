from tenacity import retry, wait_random_exponential, stop_after_attempt

from typing import List, Dict
import os
import openai
import requests

openai.api_key = ""
GPT_MODEL = "gpt-3.5-turbo-0613"  # "gpt-4-0613"


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(
    messages: str,
    functions: List[str] = None,
    function_call: Dict[str, str] = None,
    model=GPT_MODEL,
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def summarize(query: str, results: str):
    print(f"Inside Summarizing Function ---> {len(results)}")
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"""Write the summary collated from this collection of key points extracted from hackernews.
                          The summary should highlight the Abstract, Core Points and Conclusion, and answer the user's query.
                          There must be 3 line space between each highlight points. Make sure to add space in the real text and DO NOT use \n
                          User query: {query}
                          Key points:\n{results}\n 
                          """,
            }
        ],
        temperature=0,
    )
    print(f"Final Response {response}")
    return response
