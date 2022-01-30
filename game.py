from collections import defaultdict

from etc.utils import Color, read_words, get_random_word, is_valid_word
from etc.consts import MAX_ATTEMPTS, INDEX_NOT_FOUND


class WordleGame:
    _WORDS = read_words()

    def __init__(self):
        self._goal_word = ""
        self.attempts = 0
        self.word_found = False
        self.reset()

    def apply_answer(self, guess):
        if not is_valid_word(guess):
            raise ValueError("Invalid word", guess)
        elif self.attempts == MAX_ATTEMPTS:  # Lose
            return  # Nothing
        elif guess == self._goal_word:  # Win
            self.word_found = True

        self.attempts += 1

        result = []
        chars_to_idxs = self.__gen_chars_indexes_map()

        for i, _ in enumerate(guess):
            cur_char_color = self.__calc_char_color(guess, i, chars_to_idxs)

            if cur_char_color is Color.GREEN:
                chars_to_idxs[guess[i]].remove(i)
            elif cur_char_color is Color.YELLOW:
                alt_idx = self.__get_alternative_index(guess, chars_to_idxs[guess[i]])
                chars_to_idxs[guess[i]].remove(alt_idx)
            result.append(cur_char_color)

        return result

    def is_running(self):
        return not self.word_found and self.attempts < MAX_ATTEMPTS

    def reset(self):
        self._goal_word = get_random_word(self._WORDS)
        self.attempts = 0
        self.word_found = False

    def get_all_possible_words(self):
        return self._WORDS.copy()

    def is_winner(self):
        return self.word_found

    def get_answer(self):
        return self._goal_word

    def __gen_chars_indexes_map(self):
        result = defaultdict(set)

        for i, c in enumerate(self._goal_word):
            result[c].add(i)

        return result

    def __calc_char_color(self, guess, char_idx, char_to_indexes_map):
        """
        Function receives a guess that was applied as an answer, and idx of a
        letter that it's color is being evaluated and a map of chars to the
        indexes they appear in the goal word.

        There are 3 return values options:
        1. GREEN: guess matches goal at the specified index
        2. YELLOW: guess does'nt match at the specified index, but the letter
        should be somewhere else in the word
        3. GREY: specified letter is not a part of the goal word.

        :param guess: the str that was applied as an answer
        :param char_idx: the index of the char that its color is evaluated
        :param char_to_indexes_map: map of goal word's chars to their indexes
        :return: Color (GREEN, YELLOW or GREY)
        """
        result = None
        tested_char = guess[char_idx]

        if tested_char is self._goal_word[char_idx]:  # GREEN
            result = Color.GREEN
        elif tested_char not in self._goal_word:  # GREY
            result = Color.GREY
        elif tested_char in self._goal_word and char_to_indexes_map[tested_char]:  # YELLOW (possibly)
            alt_idx = self.__get_alternative_index(guess, char_to_indexes_map[tested_char])
            if alt_idx is not INDEX_NOT_FOUND:
                result = Color.YELLOW

        return result

    def __get_alternative_index(self, guess, indexes):
        for i in indexes:
            if guess[i] is not self._goal_word[i]:
                return i

        return None



