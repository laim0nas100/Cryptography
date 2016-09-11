

import re

from libs.Debug import Debug
from libs.crypt.lib import ArrayList


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


def __go(indexArrayList: ArrayList, current: ArrayList, left: ArrayList, i:int, maxLength:int):
    length = current.__len__()

    if not length < maxLength:
        indexArrayList.append(current)
        # Debug.print("add:"+current.__str__())
        return
    else:
        current.append(left.remove(i))
        length = left.__len__()
        # Debug.print("Cur:" + current.__str__() + " Left:" + left.__str__() + " len =" + str(length), end="")
        # Debug.print(" index:" + str(i))
        a = 0
        if a<length:
            while a < length:
                __go(indexArrayList,current.copy(), left.copy(), a, maxLength)
                a += 1
        else:
            indexArrayList.append(current)
            # Debug.print("add:" + current.__str__())
            return

def generateIndexList(size:int,maxLength:int)->list:
    maxLength = min(size,maxLength)
    # print("MaxLen:"+str(maxLength))
    indexArrayList = ArrayList()
    indexArray = ArrayList()

    for i in range(0, size):
        indexArray.append(i)
    for ind in range(0, maxLength):
        newArray = ArrayList()
        __go(indexArrayList, newArray.copy(), indexArray.copy(), ind, maxLength)

    return indexArrayList

def printListToFile(filePath,array:list):
    file = open(filePath,'w')
    for s in array:
        file.write(s+"\n")
    file.flush()
    file.close()

