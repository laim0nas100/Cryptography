

import re

from libs.Debug import Debug
from libs.crypt.lib import DataLine


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


def __go(indexArrayList: DataLine, current: DataLine, left: DataLine, i:int, maxLength:int):
    length = current.__len__()

    if not length < maxLength:
        indexArrayList.add(current.data)
        # Debug.print("add:"+current.__str__())
        return
    else:
        current.add(left.remove(i))
        length = left.__len__()
        # Debug.print("Cur:" + current.__str__() + " Left:" + left.__str__() + " len =" + str(length), end="")
        # Debug.print(" index:" + str(i))
        a = 0
        if a<length:
            while a < length:
                __go(indexArrayList,current.__copy__(), left.__copy__(), a, maxLength)
                a += 1
        else:
            indexArrayList.add(current.data)
            # Debug.print("add:" + current.__str__())
            return

def generateIndexList(size:int,maxLength:int)->list:
    maxLength = min(size,maxLength)
    # print("MaxLen:"+str(maxLength))
    indexArrayList = DataLine()
    indexArray = DataLine()

    for i in range(0, size):
        indexArray.add(i)
    for ind in range(0, maxLength):
        newArray = DataLine()
        __go(indexArrayList, newArray.__copy__(), indexArray.__copy__(), ind, maxLength)

    return indexArrayList.data

def printListToFile(filePath,array:list):
    file = open(filePath,'w')
    for s in array:
        file.write(s+"\n")