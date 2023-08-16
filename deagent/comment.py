from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class HighlightResult(BaseModel):
    value: str
    matchLevel: str
    matchedWords: List[str]

class Hit(BaseModel):
    created_at: str
    title: Optional[str]
    url: Optional[str]
    author: Optional[str]
    points: Optional[int]
    story_text: Optional[str]
    comment_text: Optional[str]
    num_comments: Optional[int]
    story_id: Optional[int]
    story_title: Optional[str]
    story_url: Optional[str]
    parent_id: Optional[int]
    created_at_i: int
    _tags: List[str]
    objectID: str
    _highlightResult: Dict[str, HighlightResult]

class HNResponse(BaseModel):
    hits: Optional[List[Hit]]
    nbHits: int
    page: int
    nbPages: int
    hitsPerPage: int
    exhaustiveNbHits: bool
    query: str
    params: str
    processingTimeMS: int

# Usage:
# data = requests.get(URL).json()
# parsed_data = AlgoliaHNResponse(**data)
