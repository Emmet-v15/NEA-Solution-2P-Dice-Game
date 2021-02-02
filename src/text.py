"""Library for changing colors of console text"""


"""concatenate color codes into text to change the color when it is printed"""
def red(text):
    return "\033[1;31;40m" + text + "\033[0m"


def green(text):
    return "\033[1;32;40m" + text + "\033[0m"


def orange(text):
    return "\033[1;33;40m" + text + "\033[0m"


def blue(text):
    return "\033[1;34;40m" + text + "\033[0m"
