

import re
from abc import ABC, abstractmethod

from libs.Debug import Debug
from libs.crypt.lib import ArrayList, cmp_to_key


class InputFormatter:
    alphabets = dict()
    dictionaries = dict()
    @staticmethod
    def init():
        InputFormatter.addAlphabet("en", "ABCDEFGHJIKLMNOPQRSTUVWXYZ")
        InputFormatter.addAlphabet("ltC", "AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZŽ")
        InputFormatter.addAlphabet("lt", "aąbcčdeęėfghiįyjklmnoprsštuųūvzž")
        InputFormatter.addAlphabet("slt", "ABCČDEFGHIYJKLMNOPRSTUVZŽ")

    @staticmethod
    def addAlphabet(key, alph):
        InputFormatter.alphabets.setdefault(key, alph)

    @staticmethod
    def addDictionary(key, dictionary):
        InputFormatter.dictionaries.setdefault(key,dictionary)

    @staticmethod
    def stringContainsWord(text:str,dictionary:list,wordLen=None):
        found = False
        for word in dictionary:
            if wordLen is not None:
                if len(word)>= wordLen:
                    if word in text:
                        found = True
            else:
                if word in text:
                    found = True
            if found:
                print("Found:"+word)
                return True
        return False


    @staticmethod
    def cmpByAlphabet(alphabet):
        line = ArrayList()
        line.populateFromString(alphabet)

        def cmpItems(a, b):
            index1 = line.indexOf(a)
            index2 = line.indexOf(b)
            ans = 0
            if index1 < index2:
                ans = -1
            elif index1 > index2:
                ans = 1
            return ans

        return cmpItems

    @staticmethod
    def cmpByAlphabetStr(alphabet):
        line = ArrayList()
        line.populateFromString(alphabet)

        def cmpItems(a:str, b:str):
            minLen = min(len(a),len(b))
            for i in range(0,minLen):
                index1 = line.indexOf(a[i])
                index2 = line.indexOf(b[i])
                if index1 < index2:
                    return -1
                elif index1 > index2:
                    return 1

            return 0

        return cmpItems


    @staticmethod
    def removeWithRegex(text, regex):
        return re.sub(regex, "", text)

    @staticmethod
    def removeWhiteSpace(text):
        p = re.compile(r"^\s+", re.MULTILINE)
        return p.sub("", text)

    @staticmethod
    def removeByAlphabet(text, key):
        result = ""
        alphabet = InputFormatter.alphabets.get(key)
        if alphabet is not None:
            for char in text:
                if char in alphabet:
                    result += char
        else:

            print("alphabet is None")
        return result


class WordRule(ABC):
    @abstractmethod
    def applyRule(self,text:str)->bool:
        pass

class DuplicateLetterRule(WordRule):
    def applyRule(self,text:str)->bool:
        for i in range(0,len(text)-1):
            if text[i] == text[i+1]:
                return False
            else:
                return True

class ImpossibleLetterPair(WordRule):
    def __init__(self,let1,let2):
        self.l1 = let1
        self.l2 = let2

    def applyRule(self,text:str)->bool:

        pair1 = self.l1+self.l2
        pair2 = self.l2+self.l1



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
        if "\n" not in s:
            s+="\n"
        file.write(s)
    file.flush()
    file.close()

def readListFromFile(filePath)->list:
    file = open(filePath,'r')
    array = ArrayList()
    for line in file.readlines():
        if line.__len__()>1:

            array.append(stringReplace(line,'\n'))
    return array


def stringReplace(source:str,target:str,replacement="")->str:
    if target not in source:
        return source
    try:
        index = source.index(target)
        new = source[:index] + replacement + source[len(target)+index:]
    except ValueError:
        return source
    return new



def dictionaryExtract(lines,Key=None):
    array = ArrayList()
    Set = set()
    for line in lines:
        if not line[0].isupper():
            s = line
            try:
                if "." not in s:
                    s = stringReplace(s, "dkt", ",")
                    s = stringReplace(s, "vksm", ",")
                    s = stringReplace(s, "sktv", ",")
                    s = stringReplace(s, "bdv", ",")
                    s = stringReplace(s, "prv", ",")
                    s = stringReplace(s, "jst", ",")
                    s = stringReplace(s, "įv", ",")
                    for i in s:
                        if i.isnumeric() or i == "\t" or i== "\n" or i ==" ":
                            s = stringReplace(s, i, "")
                    miniList = s.split(",")
                    for var in miniList:
                        Set.add(var)

            except ValueError:
                print(ValueError)
                pass

    for line in array:
        Set.add(line)

    array.clear()
    array.extend(Set.copy())
    array.sort(key=Key)
    return array
