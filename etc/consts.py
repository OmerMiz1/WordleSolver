# GENERAL ##

# FILES ##
WORDS_FILE_NAME = "words.txt"

#  GAME  ##
MAX_ATTEMPTS = 6
WORD_LEN = 5
VALID_WORD_RX = r"^[a-z]{5}$"
INDEX_NOT_FOUND = None

# SOLVER ##
ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
# taken from:
# https://stackoverflow.com/questions/32967395/exclude-characters-from-group-regex-while-still-looking-for-characters
EXCLUSION_RX = r"(?:(?![{chars}])[a-z])"


