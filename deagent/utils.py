from tenacity import retry, wait_random_exponential, stop_after_attempt

from typing import List, Dict
import os
import openai
import requests

openai.api_key = ""
GPT4 = "gpt-4-0613"
GPT3 = "gpt-3.5-turbo-0613"
GPT_MODEL = GPT4  # "gpt-4-0613" "gpt-3.5-turbo-0613"


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
    print(f"JSON ***** {json_data}")
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


def pdf_summarize(query: str, pdf_summary: str):
    print(f"Inside pdf_summarize @ {query} \n\n {pdf_summary}")
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"""Write a summary collated from this collection of key points extracted from an academic paper.
                            The summary should highlight the core argument, conclusions and evidence, and answer the user's query.
                            User query: {query}
                            The summary should be structured in bulleted lists following the headings Core Argument, Evidence, and Conclusions.
                            Key points:\n{pdf_summary}\nSummary:\n
                            
                            The final output must be in HTML Format and easy to read and understand by user.
                            Use different HTML styles to ensure better readability.
                            """,
            }
        ],
        temperature=0,
    )
    return response


def summarize(query: str, results: str):
    print(f"Inside Summarizing Function ---> {len(results)}")
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"""Write the summary collated from this collection of key points extracted from hackernews.
                          The summary should highlight the Summary of all topics, Core Points and Final answer to the user's query.
                          There must be 3 line space between each highlight points.
                          
                          The final output must be in HTML Format. Use different HTML styles to ensure better readability.
                          Make sure to have a list, headings and other interactive way to bring the attention on certain parts of the summary
                          The final html output must be easy to read and understand by user
                          User query: {query}
                          Key points:\n{results}\n 
                          """,
            }
        ],
        temperature=0,
    )

    return response
