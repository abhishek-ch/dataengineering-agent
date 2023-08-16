import html

import requests
from bs4 import BeautifulSoup

from deagent.comment import *
from deagent.models import *


def clean_html_data(data: str) -> str:
    soup = BeautifulSoup(data, "html.parser")
    return soup.get_text()


def remove_none_values(item: Union[Dict, List]) -> dict | list[str] | list:
    if isinstance(item, dict):
        return {
            k: remove_none_values(v) if v is not None else -1 for k, v in item.items()
        }
    elif isinstance(item, list):
        return [remove_none_values(v) for v in item]
    else:
        return item


def get_stories_from_hackernews(query: str) -> str:
    """

    :rtype: object
    """
    result = []
    response = requests.get(
        "http://hn.algolia.com/api/v1/search",
        params={"query": query.lower(), "tags": "story"},
    )

    if response.status_code == 200:
        response_data = response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        raise Exception

    # Find the first story with both 'num_comments' and 'objectID'
    first_valid_story_data = next(
        (
            story
            for story in response_data["hits"]
            if "num_comments" in story and "objectID" in story
        ),
        None,
    )

    if first_valid_story_data:
        first_story = Story(**first_valid_story_data)

        # If the story has comments, fetch the top 10 comments
        if first_story.num_comments:
            comment_response = requests.get(
                f"http://hn.algolia.com/api/v1/items/{first_story.objectID}"
            )
            comment_data = comment_response.json()

            first_story_comments = Item(**comment_data)
            # # Displaying top 10 comments (or fewer if there are not enough comments)
            for comment in first_story_comments.children[0:10]:
                if comment.text:
                    result.append(html.unescape(clean_html_data(comment.text)))
                    #
                    # print(f"FULL COMMENT {comment}")
                    # print(f"Author: {comment.author}")
                    # print(f"Text: {html.unescape(clean_html_data(comment.text))}")
                    # print(f"Date: {comment.created_at}")
                    # print("=" * 50)
    else:
        print("No valid story found with both 'num_comments' and 'objectID'")

    return "\n".join(result)


def get_comments_from_hackernews(query: str) -> str:
    print(f"Query is {query}")
    result = []
    # Fetching stories related to the query "python"
    response = requests.get(
        "http://hn.algolia.com/api/v1/search",
        params={"query": query, "tags": "comment"},
    )
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Parse the JSON data using the Pydantic model
        parsed_data = HNResponse(**data)

        # Now you can work with a well-structured object
        for hit in parsed_data.hits[:20]:
            result.append(html.unescape(clean_html_data(hit.comment_text)))
            # print(f"Author: {hit.author}")
            # print(f"Comment: {html.unescape(clean_html_data(hit.comment_text))}")
            # print("-" * 30)
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    return "\n".join(result)


def search_query_by_date(query: str) -> str:
    result = []
    base_url = "http://hn.algolia.com/api/v1/search_by_date"
    params = {"query": query}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            parsed_data = HNResponse(**data)
            # Now you can work with a well-structured object
            for hit in parsed_data.hits[:10]:
                if hit.comment_text:
                    result.append(html.unescape(clean_html_data(hit.comment_text)))
                    # print(f"Author: {hit.author} {hit.created_at}")
                    # print(f"Comment: {html.unescape(clean_html_data(hit.comment_text))}")
                    # print("-" * 30)
    else:
        print(f"Error {response.status_code}: {response.text}")

    return "\n\n\n".join(result)
