import math
from libs.crypt import IOlib
from libs.crypt.Math import Math, Matrix
from libs.crypt.lib import *


class Skytale:

    @staticmethod
    def decrypt(text, k, fromBelow = False):
        lines = ArrayList()

        for i in range(0, k):
            index = i
            lines.append("")
            while index < len(text):
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
    def getKeyArray(Key, alphabet) -> ArrayList:
        sortedKey = ArrayList()
        array = ArrayList()
        array.populateFromString(Key)
        sortedKey.populateFromString(Key)
        sortedKey.sort(key=cmp_to_key(IOlib.InputFormatter.cmpByAlphabet(alphabet)))
        keyNumbers = ArrayList()
        print(sortedKey)
        for letter in array:
            # print(" checking:"+letter,)
            number = sortedKey.indexOf(letter)
            if number not in keyNumbers:
                keyNumbers.append(number)
            else:
                keyNumbers.append(number+1)
            # print (keyNumbers.data)
        # print array.__str__()
        # print sortedKey.__str__()

        return keyNumbers

    @staticmethod
    def transpositionalTable(text:str, columnCount:int) -> Table:
        table = Table()
        index = 0
        size = text.__len__()
        columnLen = math.ceil(size/columnCount)
        while table.getLineCount() < columnLen:
            table.addLine(ArrayList())
        outOfSymbols = False
        # columnCount, columnLen = columnLen, columnCount
        for colIndex in range(0, columnCount):
            if outOfSymbols:
                break
            for lnIndex in range(0, columnLen):
                if outOfSymbols:
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

        for line in transTable.lines:
            for i in key:
                ans += line[i]

        return strKey+": "+ans

    @staticmethod
    def decryptSingle(text, key, linesAreColumns=False) -> str:
        rowLen = len(key)
        table = Transposition.transpositionalTable(text, rowLen)

        return Transposition.decrypt(table,key)

    @staticmethod
    def bruteForceSetLength(text, length, maxLength) -> ArrayList:
        indexList = IOlib.generateIndexList(length, maxLength)
        table = Transposition.transpositionalTable(text,length)
        ansList = ArrayList()
        for k in indexList:
            ansList.append(Transposition.decrypt(table, k))
        return ansList

    @staticmethod
    def bruteForceLengthInterval(text, rangeStart, rangeEnd) -> ArrayList:
        fullList = ArrayList()
        for i in range(rangeStart,rangeEnd+1):
            smallList = Transposition.bruteForceSetLength(text,i,i)
            for string in smallList:
                fullList.append(string)
        return fullList

class Fence:
    tableNullValue = "_"
    unusedCharacter= "#"
    @staticmethod
    def encrypt(text:str, k:int)-> ArrayList:
        rows = ArrayList()
        # Prepare row
        for i in range(0,k):
            row = list()
            rows.append(row)
        # bounce rows
        index =0
        increment = 1
        print("k:"+str(k))
        for char in text:
            print("index:"+str(index))
            rows[index].append(char)
            index += increment
            if index >= k:
                increment = -1
                index = k-2
            elif index < 0:
                index = 1
                increment = 1

        for r in rows:
            print(r)

        return rows




    @staticmethod
    def makeFenceTable(text:str, k:int)->Table:
        table = Table()
        table.nullValue = Fence.tableNullValue
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
        txt = ArrayList()
        txt.populateFromString(text)
        unusedChar = Fence.unusedCharacter
        table = Fence.makeFenceTable(unusedChar * size, k)
        table.equalize()
        if reverse:
            table.lines.reverse()
        for row in table.lines:
            symLen = row.count(unusedChar)
            for i in range(0,symLen):
                index = row.indexOf(unusedChar)
                row.set(index,txt.pop(0))
        line = 0
        column = 0
        increment = 1
        if reverse:
            line = size-1

        # table.printMe()
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
        return str(k)+": "+ans

    @staticmethod
    def bruteForce(text:str,rangeStart:int,rangeEnd:int,reverse=False)->list:
        fullList = ArrayList()
        for i in range(rangeStart,rangeEnd+1):
            fullList.append(Fence.decrypt(text,i,reverse))
        return fullList

class Fleissner:
    markerSymbol = "#"
    tableNullValue = "_"
    @staticmethod
    def decryptOnce(text:str,rowLen:int,Key:list, turnClockWise=True):
        Key.sort()
        table = Table.createTable(text,rowLen)
        keyTable = Table.createTable(Fleissner.tableNullValue*len(text),rowLen)
        table.equalize()
        keyTable.equalize()
        keyTable.name = "Key"
        marker = Fleissner.markerSymbol
        nullValue = Fleissner.tableNullValue
        for markerPlace in Key:
            keyTable.setFromTopLeft(markerPlace,marker)
        copy = table.__copy__()
        copy.name = "Copy"
        keyCount = Key.__len__()
        ans=""
        for turn in range(0,keyCount):

            keyTableCopy = keyTable.__copy__()
            index = keyTableCopy.indexFromTopLeft(marker)
            while index >=0:
                keyTableCopy.setFromTopLeft(index,nullValue)
                ans+= table.getFromTopLeft(index)
                index = keyTableCopy.indexFromTopLeft(marker)
            if turnClockWise:
                keyTable.rotateClockwise(1)
            else:
                keyTable.rotateCounterClockwise(1)

        return ans

class Bifid:

    @staticmethod
    def printablePairList(pairs:list):
        line1 = ""
        line2 = ""
        for i in range(0,pairs.__len__()):
            line1+=str(pairs[i][0])+","
            line2+=str(pairs[i][1])+","
        return line1+"\n"+line2

    @staticmethod
    def createBifidTable(key:str,alphabet:str)->Table:
        abc=""
        combined = key + alphabet
        for char in combined:
            if char not in abc:
                abc+=char
        # print(abc)
        table = Table()
        dim = Math.math.sqrt(abc.__len__())
        if dim - Math.math.floor(dim)!=0:
            dim = Math.math.floor(dim) + 1
        else:
            dim = Math.math.floor(dim)

        for i in range(0,abc.__len__()):
            table.set(i//dim, i % dim, abc[i])

        table.equalize()
        return table

    @staticmethod
    def createPairArray(text:str, table:Table):
        arrayList = ArrayList()
        for char in text:
            first = table.indexFromTop(char)
            second = table.indexFromLeft(char)
            pair = ArrayList()
            pair.append(first)
            pair.append(second)
            arrayList.append(pair)
        return arrayList

    @staticmethod
    def pairToLetter(pair:list,table:Table):
        return table.get(pair[0],pair[1])

    @staticmethod
    def manglePairs(pairList:ArrayList,k:int):
        l1 = ArrayList()
        l2 = ArrayList()
        line = ArrayList()
        for pairI in range(0,pairList.__len__()):
            line.append(pairList[pairI][0])
            line.append(pairList[pairI][1])
            if (1+pairI) % k==0:
                for i in range(0,line.__len__()//2):
                    l1.append(line[i])
                for i in range(line.__len__()//2,line.__len__()):
                    l2.append(line[i])
                line.clear()
        newPairList = ArrayList()
        # print(l1)
        # print(l2)
        for i in range(l1.__len__()):
            newPairList.append([l1[i], l2[i]])
        return newPairList



    @staticmethod
    def decryptSingle(text:str,k:str,alphabet:str,period:int) -> str:
        table = Bifid.createBifidTable(k, alphabet)
        pairs = Bifid.createPairArray(text, table)
        pairs = Bifid.manglePairs(pairs, period)
        string = ""
        for pair in pairs:
            string += Bifid.pairToLetter(pair, table)
        return string

class Affine:
    @staticmethod
    def charsToNumbers(text:str,alphabet:str)->list:
        array = ArrayList()
        for char in text:
            array.append(alphabet.index(char))
        return array

    @staticmethod
    def numbersToChars(array:list,alphabet:str)->str:
        string = ""
        for index in array:
            string+=alphabet[index]
        return string

    @staticmethod
    def encrypt(array:list,alpha:int,beta:int,modulus:int)->list:
        newList = ArrayList()
        for number in array:
            newList.append((number * alpha + beta) % modulus)
        return newList

    @staticmethod
    def encryptSingle(text:str,alphabet:str,alpha:int,beta:int):
        array = Affine.charsToNumbers(text,alphabet)
        newArray = Affine.encrypt(array,alpha,beta,len(alphabet))
        return Affine.numbersToChars(newArray,alphabet)

    @staticmethod
    def decrypt(array:list,alpha:int,beta:int,modulus:int)->list:
        newList = ArrayList()
        alpha = Math.multiplicativeInverse(alpha,modulus)
        for number in array:
            newList.append((alpha *(number - beta)) % modulus)
        return newList

    @staticmethod
    def decryptSingle(text:str,alphabet:str,alpha:int,beta:int):
        array = Affine.charsToNumbers(text,alphabet)
        newArray = Affine.decrypt(array,alpha,beta,len(alphabet))
        return Affine.numbersToChars(newArray,alphabet)

class Hill:


    @staticmethod
    def applyCipher(vector:Matrix, matrix:Matrix, modulus:int)->Matrix:
        def m(x):
            return int(x) % modulus
        newVector = Math.matrixMultiplication(matrix, vector)
        newVector.applyToEachElement(m)
        return newVector

    @staticmethod
    def singleCypher(text:str,matrix:Matrix,alphabet:str)->str:
        numbers = Affine.charsToNumbers(text,alphabet)
        vectors = ArrayList()
        for i in range(0,numbers.__len__(),matrix.getLineCount()):
            vector = Matrix()
            for j in range(0,2):
                vector.set(j,0,numbers[i+j])
            vectors.append(vector)
        res=""
        for i in range(0,vectors.__len__()):
            if vectors[i] is None:
                print(i)
            else:
                # print(vectors[i])
                vec = Hill.applyCipher(vectors[i], matrix, alphabet.__len__())
                for j in range(0,2):
                    res+= alphabet[vec.get(j,0)]
        return res