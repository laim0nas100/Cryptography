import math

from libs.crypt.lib import *


def __go(indexArrayList: DataLine, current: DataLine, left: DataLine, i:int, maxLength:int):
    length = current.__len__()

    if not length < maxLength:
        indexArrayList.add(current)
        print("add:"+current.__str__())
        return
    else:

        current.add(left.remove(i))
        length = left.__len__()
        print("Cur:" + current.__str__() + " Left:" + left.__str__() + " len =" + str(length), end="")
        print(" index:" + str(i))
        a = 0
        if a<length:
            while a < length:
                __go(indexArrayList,current.__copy__(), left.__copy__(), a, maxLength)
                a += 1
        else:
            indexArrayList.add(current)
            print("add:" + current.__str__())
            return

def generateIndexList(size:int,maxLength:int):
    maxLength = min(size,maxLength)
    print("MaxLen:"+str(maxLength))
    array = DataLine()
    indexArrayList = DataLine()
    indexArray = DataLine()
    for i in range(0, size):
        indexArray.add(i)
    for ind in range(0, maxLength):
        newArray = DataLine()
        __go(indexArrayList, newArray.__copy__(), indexArray.__copy__(), ind, maxLength)

    return indexArrayList

class Skytale:

    @staticmethod
    def decrypt(text, k, fromBelow = False):
        lines = list()

        for i in range(0, k):
            index = i
            lines.append("")
            while (index) < len(text):
                # print(index + i)
                lines[i] += text[index]
                index += k
        if fromBelow:
            lines.reverse()
        newstring = ""
        for ln in lines:
            newstring += ln
        return newstring

    @staticmethod
    def bruteForce(text, min, max):
        for i in range(min,max+1):
            print("number=" + str(i) +":" + Skytale.decrypt(text, i))


class Transposition:

    @staticmethod
    def cmpByAlphabet(alphabet):
        line = DataLine()
        line.populateFromString(alphabet)

        def cmpItems(a, b):
            index1 = line.data.index(a)
            index2 = line.data.index(b)
            ans = 0
            if index1 < index2:
                ans = -1
            elif index1 > index2:
                ans = 1
            return ans
        return cmpItems

    @staticmethod
    def getKeyArray(key, alphabet):
        sortedKey = DataLine()
        array = DataLine()
        array.populateFromString(key)
        sortedKey.populateFromString(key)
        sortedKey.data.sort(key=cmp_to_key(Transposition.cmpByAlphabet(alphabet)))
        keyNumbers = DataLine()
        print(sortedKey.data)
        i = 0

        for letter in array.data:
            # print(" checking:"+letter,)
            number = sortedKey.indexOf(letter)
            if not number in keyNumbers.data:
                keyNumbers.add(number)
            else:
                keyNumbers.add(number+1)
            # print (keyNumbers.data)
        # print array.__str__()
        # print sortedKey.__str__()

        return keyNumbers.data
    @staticmethod
    def transpositionalTable(text:str, columnCount:int):
        table = Table()
        index = 0
        size = text.__len__()
        columnLen = math.ceil(size/columnCount)
        while table.getLineCount() < columnLen:
            table.addLine(DataLine())
        outOfSymbols = False
        # columnCount, columnLen = columnLen, columnCount
        for colIndex in range(0, columnCount):
            if(outOfSymbols):
                break
            for lnIndex in range(0, columnLen):
                if (outOfSymbols):
                    break
                table.set(lnIndex, colIndex, text[index])
                index+=1
                if not (index < size):
                    outOfSymbols = True

        table.equalize()
        return table


    @staticmethod
    def transpositionSingle(text, key, linesAreColumns=False):
        rowLen = len(key)
        table = Transposition.transpositionalTable(text, rowLen)
        table.equalize()
        # Reading table
        ans =""
        for line in table.data:
            for i in key:
                ans += line.data[i]

        table.printMe()
        return ans
