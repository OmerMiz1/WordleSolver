import random
import re
from enum import Enum

from etc.consts import WORDS_FILE_NAME, VALID_WORD_RX


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
    words_set = set()

    with open(WORDS_FILE_NAME, "r") as words_file:
        for line in words_file.readlines():  # each line is a single word
            word = line.strip().lower()

            if word not in words_set and is_valid_word(word):
                words_set.add(word)

    return list(words_set)


def is_valid_word(word):
    """
    Function takes a string (word), and checks if it is a lower-case, letters
    only string. If it is, returns true.

    :param word: the word being validated
    :return: bool
    """
    return re.fullmatch(VALID_WORD_RX, word) is not None


def count_unique_chars(word):
    """
    Function returns the number of unique (different) chars withing a given str
    (word).

    :param word: the str that its unique chars is being counted.
    :return: number (int)
    """
    return len(set(word))
