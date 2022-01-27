from etc.utils import Color, count_unique_chars
from etc.consts import EXCLUSION_RX, WORD_LEN, ALPHABET_LOWER
from players.interface_player import IPlayer
import re


class ComputerPlayer(IPlayer):
    def __init__(self):
        self.possible_words = []
        self.grey_chars = []
        self.yellow_chars = r""

    def solve(self, game):
        self.reset()
        self.possible_words = game.get_all_possible_words()

        while game.is_running():
            try:  # both funcs throw the same error (diff message)
                guess = self.__calc_next_guess()
                colors = game.apply_answer(guess)
            except ValueError as e:
                print(e)
                return

            if colors:
                self.__update_elimination_rules(guess, colors)
                self.__eliminate_words(guess, colors)

    def reset(self):
        self.grey_chars = {i: r"" for i in range(WORD_LEN)}
        self.yellow_chars = r""
        self.possible_words = []

    def __update_elimination_rules(self, guess, colors):
        """
        After applying a guess, this function should be used to update
        the grey and yellow chars. These variables are later used to decide
        which words should be eliminated from the possible words list.
        The grey chars will be used to generate a regex, the yellow chars are a
        list of required chars.

        :param guess: The guess applied to the game object.
        :param colors: Result received from game object after applying guess.
        :return: Nothing
        """
        # Update green, yellow & grey chars
        for i, c in enumerate(colors):
            if c is Color.GREY:
                for j in range(WORD_LEN):
                    self.grey_chars[j] += guess[i]
            elif c is Color.YELLOW:
                self.grey_chars[i] += guess[i]
                self.yellow_chars += guess[i]

    def __eliminate_words(self, guess, colors):
        rx = r""

        # Build regex (for eliminating impossible words)
        for i, color in enumerate(colors):
            if color is Color.GREEN:  # i'th letter is known
                rx += guess[i]
            else:
                rx += EXCLUSION_RX.format(chars=self.grey_chars[i])

        # Filter function
        regex_filter = lambda word: re.search(rx, word)
        yellow_filter = lambda word: self.__contains_all_yellow_chars(word)
        both_filter = lambda word: (regex_filter(word) and yellow_filter(word))

        # Eliminate impossible words
        self.possible_words[::] = list(filter(both_filter, self.possible_words))

    def __calc_next_guess(self):
        """
        The logic of choosing a guess.
        First we calculate chars frequencies so we can value each word. The more
        frequent a word's chars the higher her score. Eventually we choose the
        word with the highest value as our next guess.
        That way we can try to eliminate as many words as possible for our next
        guess.

        :return: string, the guess that should be applied this turn.
        """
        chars_frequencies = self.__calc_chars_frequency(self.possible_words)

        word_value_fn = lambda word: self.__word_value(word, chars_frequencies, self.yellow_chars)
        self.possible_words.sort(key=word_value_fn)
        if self.possible_words:
            return self.possible_words.pop()
        else:
            raise ValueError("Words list is empty")

    def __contains_all_yellow_chars(self, word):
        """
        Tells if given word contains all yellow chars.

        :param word: tested word
        :return: Bool
        """
        yellow_chars_list = list(self.yellow_chars)  # Stack
        word_copy = word

        while yellow_chars_list:
            char = yellow_chars_list.pop()
            if char not in word_copy:
                return False
            word_copy.replace(char, "", 1)

        return True

    @staticmethod
    def __calc_max_unique_chars(words):
        """
        Calculate the word with most unique chars in a given words list

        :param words: The list
        :return: number of max unique chars in a word in words.
        """
        result = 0

        if words:
            str_max_unique_chars = max(words, key=count_unique_chars)
            result = len(set(str_max_unique_chars))

        return result

    @staticmethod
    def __calc_chars_frequency(words):
        frequencies = {char: 0 for char in ALPHABET_LOWER}

        for word in words:
            for char in word:
                frequencies[char] += 1

        return frequencies

    @staticmethod
    def __word_value(word, frequencies, yellow_chars):
        """
        Calculates a word's value as a function of its chars, unique chars and
        the frequency of each contained char.
        The Higher the score the more likely we want to choose the word.

        :param word: the word we value
        :param frequencies: map of chars to their frequencies (in possible words)
        :param yellow_chars: string of all required chars
        :return: a numeric value, the higher the better.
        """
        word_value = 0
        max_freq = frequencies[max(frequencies)]

        for char in word:
            word_value += frequencies[char]
            if char in yellow_chars:  # Give extra points to increase prob
                word_value += max_freq

        word_value /= (WORD_LEN - count_unique_chars(word) + 1)
        return word_value
