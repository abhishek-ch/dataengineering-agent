hnapi_functions = [
    {
        "name": "get_stories_from_hackernews",
        "description": """Use this function to get stories from Hackernewsfor the query and summarize the response""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                              User query as string. Responses should be summarized
                              """,
                }
            },
            "required": ["query"],
        },
        "name": "get_comments_from_hackernews",
        "description": """Use this function to read all comments for the query and summarize the response as list""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                     User query as string. Responses should be summarized
                    """,
                }
            },
            "required": ["query"],
        },
        "name": "search_query_by_date",
        "description": """Use this function to read info related to the query Sorted by date, more recent first using algolia api.
    You should highlight all important points as list. Make sure to summarize the final response as list""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                         User query as string. Responses should be summarized
                        """,
                }
            },
            "required": ["query"],
        },
        #         "name": "get_comments_by_time",
        #         "description": """Use this function to read info within a specific timerange using algolia api and summarize the response.
        # You should highlight all important points as list""",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "tags": {
        #                     "type": "string",
        #                     "description": f"""Available tags:
        #                                     story
        #                                     comment
        #                                     poll
        #                                     pollopt
        #                                     show_hn
        #                                     ask_hn
        #                                     front_page
        #                                     author_:USERNAME
        #                                     story_:ID""",
        #                 },
        #                 "start_time": {
        #                     "type": "string",
        #                     "description": f"""
        #                      Start timestamp (created_at_i > X)
        #                     """,
        #                 },
        #                 "end_time": {
        #                     "type": "string",
        #                     "description": f"""
        #                      nd timestamp (created_at_i < Y)
        #                     """,
        #                 }
        #             },
        #             "required": ["tags","start_time","end_time"],
        #         },
    }
]
