import random
from collections import defaultdict

from etc.utils import CharSpotInWord, get_random_file_line, is_valid_word, read_words_from_file
from etc.consts import MAX_ATTEMPTS, INDEX_NOT_FOUND, WORDS_FILE_NAME


class WordleGame:
    def __init__(self):
        self._goal_word = None
        self.attempts = None
        self.word_found = None
        self.reset()

    def apply_answer(self, guess):
        if not is_valid_word(guess):
            raise ValueError("Invalid word: ", guess)
        elif self.attempts == MAX_ATTEMPTS:  # Lose
            return  # Nothing
        elif guess == self._goal_word:  # Win
            self.word_found = True

        self.attempts += 1

        result = []
        chars_to_indexes = self._gen_chars_indexes_map()

        for i, _ in enumerate(guess):
            char_spot = self._evaluate_char_spot(guess, i, chars_to_indexes)

            if char_spot is CharSpotInWord.CORRECT:
                chars_to_indexes[guess[i]].remove(i)
            elif char_spot is CharSpotInWord.WRONG_SPOT:
                alternative_index = self._get_alternative_index(guess, chars_to_indexes[guess[i]])
                chars_to_indexes[guess[i]].remove(alternative_index)
            result.append(char_spot)

        return result

    def is_running(self):
        return not self.word_found and self.attempts < MAX_ATTEMPTS

    def reset(self):
        self._goal_word = get_random_file_line(WORDS_FILE_NAME)
        self.attempts = 0
        self.word_found = False

    @staticmethod
    def get_all_possible_words():
        return read_words_from_file(WORDS_FILE_NAME)

    def is_winner(self):
        return self.word_found

    def get_answer(self):
        return self._goal_word

    def _gen_chars_indexes_map(self):
        result = defaultdict(set)

        for i, c in enumerate(self._goal_word):
            result[c].add(i)

        return result

    def _evaluate_char_spot(self, guess, char_index, char_to_indexes_map):
        """
        Function receives a guess that was applied as an answer, and idx of a
        letter that it's correctness is being evaluated and a map of chars to the
        indexes they appear in the goal word.

        :param guess: the str that was applied as an answer
        :param char_index: the index of the char that its correctness is evaluated
        :param char_to_indexes_map: map of goal word's chars to their indexes
        :return: Enum, CharSpotInWord (see utils.py)
        """
        tested_char = guess[char_index]

        if tested_char is self._goal_word[char_index]:
            result = CharSpotInWord.CORRECT
        elif tested_char not in self._goal_word:
            result = CharSpotInWord.NOT_IN_WORD
        else:  # tested char is somewhere else in goal word
            alternative_index = self._get_alternative_index(guess, char_to_indexes_map[tested_char])
            if alternative_index is not INDEX_NOT_FOUND:
                result = CharSpotInWord.WRONG_SPOT
            else:  # In goal word, but redundant duplicate
                result = CharSpotInWord.NOT_IN_WORD

        return result

    def _get_alternative_index(self, guess, indexes):
        for i in indexes:
            if guess[i] is not self._goal_word[i]:
                return i

        return None



