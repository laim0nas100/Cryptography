import math

import numpy

from libs.crypt.lib import Table

class Matrix(Table):

    def __init__(self):
        super().__init__()


class Math:
    math = math
    @staticmethod
    def multiplicativeInverse(number: int, modulus: int) -> int:
        for i in range(0,modulus):
            ans = i * number % modulus
            if ans == 1:
                return i
            else:
                i += 1
        return None

    @staticmethod
    def matrixAddition(m1:Matrix, m2:Matrix) -> Matrix:
        m3 = Matrix()
        for i in range(0,m1.getCellCount()):
            value = m1.getFromTopLeft(i) + m2.getFromTopLeft(i)
            m3.setFromTopLeft(i,value)
        return m3

    @staticmethod
    def matrixProduct(m1:Matrix, number):
        m3 = Matrix()

        for i in range(0, m1.getCellCount()):
            value = m1.getFromTopLeft(i) * number
            m3.setFromTopLeft(i, value)
        return m3

    @staticmethod
    def matrixMultiplication(m1:Matrix, m2:Matrix) -> Matrix:
        m3 = Matrix()
        for i in range(0,m1.getCellCount()):
            value = m1.getFromTopLeft(i) + m2.getFromTopLeft(i)
            m3.setFromTopLeft(i,value)
        return m3
