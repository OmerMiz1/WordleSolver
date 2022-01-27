from etc.utils import Color, read_words, get_random_word, is_valid_word
from collections import defaultdict
from etc.consts import MAX_ATTEMPTS, INDEX_NOT_FOUND


class WordleGame:
    words = read_words()

    def __init__(self):
        self.__goal_word = ""
        self.attempts = 0
        self.word_found = False
        self.reset()

    def apply_answer(self, guess):
        result = None

        if not is_valid_word(guess):
            raise ValueError("Invalid word", guess)
        elif self.attempts is MAX_ATTEMPTS:  # Lose
            return  # Nothing
        elif guess == self.__goal_word:
            self.attempts += 1
            self.word_found = True
        else:
            result = []
            chars_to_idxs = self.__gen_chars_indexes_map()

            for i, _ in enumerate(guess):
                cur_color = self.__calc_char_color(guess, i, chars_to_idxs)

                if cur_color is Color.GREEN:
                    chars_to_idxs[guess[i]].remove(i)
                elif cur_color is Color.YELLOW:
                    alt_idx = self.__get_alternative_index(guess, chars_to_idxs[guess[i]])
                    chars_to_idxs[guess[i]].remove(alt_idx)
                result.append(cur_color)

        self.attempts += 1
        return result

    def is_running(self):
        return not self.word_found and self.attempts < MAX_ATTEMPTS

    def reset(self):
        self.__goal_word = get_random_word(self.words)
        self.attempts = 0
        self.word_found = False

    def get_all_possible_words(self):
        return self.words.copy()

    def is_winner(self):
        return self.word_found

    def get_answer(self):
        return self.__goal_word

    def __gen_chars_indexes_map(self):
        result = defaultdict(set)

        for i, c in enumerate(self.__goal_word):
            result[c].add(i)

        return result

    def __calc_char_color(self, guess, idx, char_to_idxs):
        result = None
        char = guess[idx]

        if char is self.__goal_word[idx]:  # GREEN
            result = Color.GREEN
        elif char not in self.__goal_word:  # GREY
            result = Color.GREY
        elif char in self.__goal_word and char_to_idxs[char]:  # YELLOW (possibly)
            alt_idx = self.__get_alternative_index(guess, char_to_idxs[char])
            if alt_idx is not INDEX_NOT_FOUND:
                result = Color.YELLOW

        return result

    def __get_alternative_index(self, guess, indexes):
        for i in indexes:
            if guess[i] is not self.__goal_word[i]:
                return i

        return None



