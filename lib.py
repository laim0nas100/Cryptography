# coding=utf-8
def utfPrint(text):
    print(text, "utf-8")

def formatListToString(array):
    string = ""
    for x in array:
        if x is None:
            x = " "

        string += str(x)+u","

    return "["+string[:-1] + "]"


class Object:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return "name=" + str(self.name) + " value=" + str(self.value)


class DataLine:
    def __init__(self, nullValue=" "):
        self.data = []
        self.nullValue = nullValue
    def __len__(self):
        return len(self.data)

    def __fitsInRange(self, index:int):
        if len(self.data) <= index:
            return False
        else:
            return True

    def appendToSize(self, requiredSize):
        while  self.__len__() < requiredSize:
            self.data.append(self.nullValue)

    def add(self, value, index=None):
        if index is None:
            self.data.append(value)
        elif not self.__fitsInRange(index):
            self.appendToSize(index)
            self.data.append(value)
        else:
            self.data.insert(index, value)

    def set(self, index, value):
        if not self.__fitsInRange(index):
            self.appendToSize(index+1)
        self.data[index] = value

    def indexOf(self, value):
        i = -1
        for val in self.data:
            i+=1
            if value == val:
                return i
        return -1

    def remove(self, index):
        ob = self.data[index]
        del self.data[index]
        return ob

    def __copy__(self):
        line = DataLine()
        for ob in self.data:
            line.add(ob)
        return line

    def populateFromString(self, text):

        for i in text:
            self.add(i)

    def __str__(self):
        return formatListToString(self.data)


class Table:
    def __init__(self, data=None):
        self.data = []
        self.name = "Table"
        self.nullValue =""
        if data is not None:
            self.data.extend(data)

    def equalize(self):
        maxTableLen = 0
        for line in self.data:
            if maxTableLen < line.__len__():
                maxTableLen = line.__len__()
        for line in self.data:
            line.appendToSize(maxTableLen)

    def addLine(self, line):
        self.data.append(line)

    def remove(self, line, column):
        ob = self.data[line].data[column]
        del self.data[line].data[column]
        return ob

    def get(self, line, column):
        ob = self.data[line].data[column]
        return ob

    def set(self, line: int, column: int, value):
        while line >= self.getLineCount():
            self.addLine(DataLine(self.nullValue))
        self.data[line].set(column, value)

    def getLineCount(self):
        return self.data.__len__()

    def getColumnCount(self):
        self.equalize()
        if self.getColumnCount()>0:
            return self.data.__len__()
        else:
            return 0

    def __str__(self):
        string = self.name+u"\n"
        for line in self.data:
            string += line.__str__()+u"\n"
        return string

    def printMe(self):
        print (self.name)
        for line in self.data:
            print (line.__str__())

    @staticmethod
    def createTable(text, lineLength, linesAreColumns=False):
        table = Table()
        index = 0
        lineIndex = 0
        origline = DataLine()
        for i in text:
            origline.add(i)
        line = DataLine()
        size = origline.data.__len__()

        if not linesAreColumns:
            while index < size:
                if lineIndex >= lineLength:
                    table.addLine(line)
                    line = DataLine()
                    lineIndex = 0
                line.set(lineIndex, origline.data[index])
                index += 1
                lineIndex += 1
            table.addLine(line)
        else:
            while table.getLineCount()<lineLength:
                table.addLine(DataLine())
            currentIndex = 0
            while index < size:
                if lineIndex >= lineLength:
                    lineIndex = 0
                    currentIndex+=1
                table.set(lineIndex, currentIndex, origline.data[index])
                index += 1
                lineIndex += 1
        return table


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K