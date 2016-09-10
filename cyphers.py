import math

from libs.crypt import IOlib
from libs.crypt.lib import *




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
            print(str(i) +": " + Skytale.decrypt(text, i))


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
    def getKeyArray(key, alphabet) -> list:
        sortedKey = DataLine()
        array = DataLine()
        array.populateFromString(key)
        sortedKey.populateFromString(key)
        sortedKey.data.sort(key=cmp_to_key(Transposition.cmpByAlphabet(alphabet)))
        keyNumbers = DataLine()
        print(sortedKey.data)
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
    def transpositionalTable(text:str, columnCount:int) -> Table:
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
    def decrypt(transTable:Table, key:list) -> str:
        ans = ""
        strKey = ""
        for i in key:
            strKey+= str(i)

        for line in transTable.data:
            for i in key:
                ans += line.data[i]


        return strKey+": "+ans

    @staticmethod
    def decryptSingle(text, key, linesAreColumns=False) -> str:
        rowLen = len(key)
        table = Transposition.transpositionalTable(text, rowLen)

        return Transposition.decrypt(table,key)

    @staticmethod
    def bruteForceSetLength(text, length, maxLength) -> list:
        indexList = IOlib.generateIndexList(length, maxLength)
        table = Transposition.transpositionalTable(text,length)
        ansList = list()
        for k in indexList:
            ansList.append(Transposition.decrypt(table, k))
        return ansList

    @staticmethod
    def bruteForceLengthInterval(text, rangeStart, rangeEnd):
        fullList = list()
        for i in range(rangeStart,rangeEnd+1):
            smallList = Transposition.bruteForceSetLength(text,i,i)
            for str in smallList:
                fullList.append(str)
        return fullList

class Fence:

    @staticmethod
    def encrypt(text:str, k:int)-> DataLine:
        rows = DataLine()
        # Prepare row
        for i in range(0,k):
            row = list()
            rows.add(row)
        # bounce rows
        index =0
        increment = 1
        print("k:"+str(k))
        for char in text:
            print("index:"+str(index))
            rows.data[index].append(char)
            index += increment
            if index >= k:
                increment = -1
                index = k-2
            elif index < 0:
                index = 1
                increment = 1


        for r in rows.data:
            print(r)

        return rows




    @staticmethod
    def makeFanceTable(text:str, k:int)->Table:
        table = Table()
        table.nullValue ="_"
        line = 0
        column = 0
        increment = 1
        for char in text:
            table.set(line,column,char)
            column+=1
            line += increment
            if line >= k:
                increment = -1
                line = k - 2
            elif line < 0:
                line = 1
                increment = 1
        return table

    @staticmethod
    def decrypt(text: str, k: int, reverse=False) -> str:
        ans=""
        size = len(text)
        txt = DataLine()
        txt.populateFromString(text)
        table = Fence.makeFanceTable("#" * size, k)
        table.equalize()
        if(reverse):
            table.data.reverse()
        for row in table.data:
            symLen = row.data.count("#")
            for i in range(0,symLen):
                index = row.indexOf("#")
                row.set(index,txt.remove(0))
        line = 0
        column = 0
        increment = 1
        if reverse:
            line = size-1

        table.printMe()
        while column < size:
            ans+= table.get(line,column)
            column += 1
            line += increment
            if line >= k:
                increment = -1
                line = k - 2
            elif line < 0:
                line = 1
                increment = 1
        return str(k)+";"+ans

    @staticmethod
    def bruteForce(text:str,rangeStart:int,rangeEnd:int,reversed=False)->list:
        fullList = list()
        for i in range(rangeStart,rangeEnd+1):
            fullList.append(Fence.decrypt(text,i,reversed))
        return fullList