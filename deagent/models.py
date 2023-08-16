from typing import List, Optional, Union

from pydantic import BaseModel


class HighlightResult(BaseModel):
    value: str
    matchLevel: str
    matchedWords: List[str]


class UserHighlight(BaseModel):
    user: HighlightResult


class StoryHighlight(BaseModel):
    title: HighlightResult
    url: HighlightResult


class Comment(BaseModel):
    id: int
    created_at: str
    created_at_i: int
    type: str
    author: Optional[str]
    text: Optional[str]
    parent_id: Optional[int]
    story_id: Optional[int]
    _highlightResult: Optional[UserHighlight]


class Item(BaseModel):
    id: int
    created_at: str
    created_at_i: int
    type: str
    author: str
    title: str
    url: str
    text: Optional[str]
    points: Optional[int]
    story_id: Optional[int]
    parent_id: Optional[int]
    children: List[Union[Comment, "Item"]]  # Recursive
    _highlightResult: Optional[StoryHighlight]


Item.update_forward_refs()


class Story(BaseModel):
    # id: Optional[int]
    # type: Optional[str]
    # text: Optional[str]
    created_at: str
    title: str
    url: str
    author: str
    points: int
    story_text: Optional[str]
    comment_text: Optional[str]
    num_comments: int
    story_id: Optional[int]
    story_title: Optional[str]
    story_url: Optional[str]
    parent_id: Optional[int]
    created_at_i: int
    # relevancy_score: Optional[int]
    _tags: List[str]
    objectID: str
    _highlightResult: StoryHighlight


class SearchResult(BaseModel):
    hits: List[Story]
    nbHits: int
    page: int
    nbPages: int
    hitsPerPage: int
    exhaustiveNbHits: bool
    query: str
    params: str
    processingTimeMS: int


# Comment.model_rebuild()
