import random
import re
from enum import Enum

from etc.consts import VALID_WORD_RX


class CharSpotInWord(Enum):
    CORRECT = 0
    WRONG_SPOT = 1
    NOT_IN_WORD = 2


def get_random_file_line(file_path):
    """
    Returns a random line within a file.

    :param file_path: path to the target file
    :return: string (random line from the file)
    """
    words_count = count_file_lines(file_path)
    random_line_number = random.randint(0, words_count - 1)

    return read_line_from_file(file_path, random_line_number)


def read_words_from_file(file_path):
    """
    Reads all words from the text file defined in etc\consts.py file.
    :return: List of words
    """
    words_set = set()

    with open(file_path, "r") as words_file:
        for line in words_file.readlines():  # each line is a single word
            word = line.strip().lower()

            if word not in words_set and is_valid_word(word):
                words_set.add(word)

    return list(words_set)


def read_line_from_file(file_path, line_number):
    file_lines_count = count_file_lines(file_path)
    if line_number > file_lines_count-1:
        raise Exception(f"Invalid line number: ", line_number, file_lines_count)

    with open(file_path, "r") as file:
        word = file.readlines()[line_number]
        return word.strip().lower()


def count_file_lines(file_path):
    with open(file_path, "r") as file:
        return len(file.readlines())


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
