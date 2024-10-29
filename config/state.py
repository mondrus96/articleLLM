from typing import TypedDict

# Writing state
class WritingState(TypedDict):
    # Processing and summarizing
    scraped: str
    notes: str
    cleaned: str
    summarized: str

    # Full article
    full: str
    short: str