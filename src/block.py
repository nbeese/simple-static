from enum import Enum

class BlockType(Enum):
    PLAIN = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"
