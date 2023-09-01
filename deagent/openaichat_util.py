import json
from typing import List
import pprint
from deagent.hnapi import (
    get_stories_from_hackernews,
    get_comments_from_hackernews,
    search_query_by_date,
)
from deagent.utils import chat_completion_request, summarize, pdf_summarize
from deagent.pdfreader_util import process_pdf, summarize_chunk


def chat_completion_with_function_execution(messages, functions: List[str] = [None]):
    """This function makes a ChatCompletion API call with the option of adding functions"""
    response = chat_completion_request(messages, functions)
    print(f"Response from chat completion {response.json()}")
    if "choices" in response.json():
        full_message = response.json()["choices"][0]
        if full_message["finish_reason"] == "function_call":
            func_call = full_message["message"]["function_call"]
            func_call_name = func_call["name"]
            func_call_arg = func_call["arguments"]
            print(f"The Actual Function call \n{func_call} name: {func_call_name} args {func_call_arg}")
            return call_hnapi_function(messages, full_message), func_call_name
    else:
        print(f"Function not required, responding to user or no choices")
        return response["choices"][0]["message"], "No function Call"


def call_hnapi_function(messages, full_message) -> str:
    """Function calling function which executes function calls when the model believes it is necessary.
    Currently extended by adding clauses to this if statement."""

    func_name = full_message["message"]["function_call"]["name"]
    parsed_output = json.loads(
        full_message["message"]["function_call"]["arguments"]
    )
    match func_name:
        case "process_pdf":
            processed_result = summarize_chunk(process_pdf(parsed_output["pdf_name"]))
            # print(f"processed_result ==> {processed_result}")
            summary = pdf_summarize(parsed_output["pdf_name"], processed_result)
            if summary:
                result = summary["choices"][0]["message"]["content"]
                return result
        case "get_stories_from_hackernews":
            try:

                print("Getting search results")
                results = get_stories_from_hackernews(parsed_output["query"])
            except Exception as e:
                print(parsed_output)
                print(f"Function execution failed")
                print(f"Error message: {e}")

            try:
                print("Got search results, summarizing content")
                response = chat_completion_request(messages)
                return response.json()
            except Exception as e:
                print(type(e))
                raise Exception("Function chat request failed")
        case "get_comments_from_hackernews":
            print("Extracting Comments")
            full_news = get_comments_from_hackernews(parsed_output["query"])
            return full_news
        case "search_query_by_date":
            print("Extracting Comments")
            full_result = search_query_by_date(parsed_output["query"])
            print("Summarizing the Result")

            summary = summarize(parsed_output["query"], full_result)
            if summary:
                result = summary["choices"][0]["message"]["content"]
                return result
        case _:
            raise NotImplemented("Function does not exist and cannot be called")


# if __name__ == '__main__':
#     hn_system_message = """You are a DataEngineering Agent, a helpful assistant reads hackernews to answer user questions.
#     You summarize the hackernews stories and comments clearly so the customer can decide which to read to answer their question.
#     You provide hn link so the user can understand the name of the topic and click through to access it.
#     Begin!"""
#     hn_conversation = Conversation()
#     hn_conversation.add_message("system", hn_system_message)
#
#     # Add a user message
#     hn_conversation.add_message("user", "What is the recent news about vector database?")
#     chat_response = chat_completion_with_function_execution(
#         hn_conversation.conversation_history, functions=hnapi_functions
#     )
#     # if (chat_response.get('function_call')):
#     #     pprint(chat_response.get('function_call'))
#     # print(chat_response)
#     # assistant_message = chat_response["choices"][0]["message"]["content"]
#     hn_conversation.add_message("assistant", chat_response)
#     print(chat_response)
#     # display(Markdown(assistant_message))
