from typing import List


def white_space_tokenizer(text: str) -> List[str]:
    tokens = text.strip().split(" ")
    return tokens
