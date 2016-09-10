

import re


class InputFormatter:

    def __init__(self):
        self.alphabets = dict()

    def addAlphabet(self, key, alph):
        self.alphabets.setdefault(key, alph)

    @staticmethod
    def removeWithRegex(text, regex):
        return re.sub(regex, "", text)

    @staticmethod
    def removeWhiteSpace(text):
        p = re.compile(r"^\s+", re.MULTILINE)
        return p.sub("", text)

    def removeByAlphabet(self, text, key):
        result = ""
        alphabet = self.alphabets.get(key)
        if alphabet is not None:
            for char in text:
                if char in alphabet:
                    result += char
        else:
            print("alphabet is None")
        return result


