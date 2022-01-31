import string

# GENERAL ##

# FILES ##
WORDS_FILE_NAME = "words_filtered.txt"

#  GAME  ##
MAX_WORD_GUESSES = 6
WORD_LEN = 5
VALID_WORD_REGEX = r"^[a-z]{5}$"
INDEX_NOT_FOUND = None

# SOLVER ##
ALPHABET_LOWER = string.ascii_lowercase
# The regex takes chars variable as format argument. chars specifies which
# chars must not be in the string.
# For example, if chars="abc", then the regex will only match if any of d-z will
# be present.
# taken from:
# https://stackoverflow.com/questions/32967395/exclude-characters-from-group-regex-while-still-looking-for-characters
EXCLUSION_RX = r"(?:(?![{chars}])[a-z])"
