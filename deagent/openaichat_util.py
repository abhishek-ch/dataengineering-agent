import json
from typing import List

from deagent.hnapi import (
    get_stories_from_hackernews,
    get_comments_from_hackernews,
    search_query_by_date,
)
from deagent.utils import chat_completion_request, summarize


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
            # pprint(f"The Actual Function call \n{func_call}")
            print(
                f"Function generation requested, calling function {func_call_name} args {func_call_arg}"
            )
            return call_hnapi_function(messages, full_message)
    else:
        print(f"Function not required, responding to user or no choices")
        return response.json()


def call_hnapi_function(messages, full_message):
    """Function calling function which executes function calls when the model believes it is necessary.
    Currently extended by adding clauses to this if statement."""

    if (
        full_message["message"]["function_call"]["name"]
        == "get_stories_from_hackernews"
    ):
        try:
            parsed_output = json.loads(
                full_message["message"]["function_call"]["arguments"]
            )
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

    elif (
        full_message["message"]["function_call"]["name"]
        == "get_comments_from_hackernews"
    ):
        parsed_output = json.loads(
            full_message["message"]["function_call"]["arguments"]
        )
        print("Extracting Comments")
        full_news = get_comments_from_hackernews(parsed_output["query"])
        return full_news
    elif full_message["message"]["function_call"]["name"] == "search_query_by_date":
        parsed_output = json.loads(
            full_message["message"]["function_call"]["arguments"]
        )
        print("Extracting Comments")
        full_result = search_query_by_date(parsed_output["query"])
        print("Summarizing the Result")

        summary = summarize(parsed_output["query"], full_result)
        if summary:
            return summary["choices"][0]["message"]["content"].replace("\n", "")
            # return summary
    else:
        raise Exception("Function does not exist and cannot be called")


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
