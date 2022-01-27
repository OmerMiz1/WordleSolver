from etc.consts import WORDS_FILE_NAME, VALID_WORD_RX
from enum import Enum
import random
import re


class Color(Enum):
    GREY = 0
    YELLOW = 1
    GREEN = 2


def get_random_word(words):
    """
    Given a list of words, returns a random word.

    :param words: list of words (strings)
    :return: a random word from words list
    """
    if not words:
        raise Exception("Words list is empty!", words)

    rand_idx = random.randint(0, len(words)-1)
    return words[rand_idx]


def read_words():
    """
    Reads all words from the text file defined in etc\consts.py file.
    :return: List of words
    """
    result = []

    with open(WORDS_FILE_NAME, "r") as words_file:
        for line in words_file.readlines():  # each line is a single word
            word = line.strip()
            if is_valid_word(word):
                result.append(word)

    return result


def is_valid_word(word):
    return re.fullmatch(VALID_WORD_RX, word) is not None


def count_unique_chars(word):
    return len(set(word))
