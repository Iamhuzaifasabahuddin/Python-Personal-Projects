import numpy as np
import random


class Operator:
    def __init__(self, num1, num2):
        try:
            assert type(num1) == int or type(num1) == float
            assert type(num2) == int or type(num2) == float
            self.num1 = num1
            self.num2 = num2
        except AssertionError:
            print("Numbers should be either int or float")

    def __str__(self):
        return f"This is an operator class and numbers being inputted are {float(self.num1),float(self.num2)}"

    def __add__(self):
        addition = self.num1 + self.num2
        return f"Sum of addition is {addition}"

    def __sub__(self):
        subtraction = self.num2 - self.num1
        return f"Subtraction of Num 2 - Num 1 is {subtraction}"

    def __mul__(self):
        multiplication = self.num1 * self.num2
        return f"Product of two numbers is {multiplication}"

    def __div__(self):
        try:
            division = self.num2 / self.num1
            division = format(division, ".3f")
            return f"Division of {self.num2} / {self.num1} is {float(division)}"
        except ZeroDivisionError:
            return np.nan, "Number cant be divided by zero "

    def __pow__(self, other=0):
        try:
            if other == 0:
                power = self.num1 ** self.num2
                power = format(power, ".3f")
                return f"{self.num1} raise to the power of {self.num2} is {float(power)}"
            else:
                power = self.num1 * other
                power = format(power, ".3f")
                power2 = self.num2 * other
                power2 = format(power2, ".3f")
                return f"Num1 raise to the power of {other} is {float(power)} " \
                       f"and Num2 raise to the power of {other} is {float(power2)}"
        except:
            print("Number cant be raised to the power")

    def equal(self):
        if self.num1 == self.num2:
            return f"Both given numbers {self.num1} and {self.num2} are equal"
        else:
            return f"Both given numbers {self.num1} and {self.num2} are not equal"

    def percentage(self, percent=0):
        if percent == 0:
            per = self.num1 * (self.num2/100)
            per = format(per, ".3f")
            return f"{self.num2} % of {self.num1} of is {float(per)}"
        else:
            per1 = self.num1 * (percent/100)
            per2 = self.num2 * (percent/100)
            per1 = format(per1, ".3f")
            per2 = format(per2, ".3f")
            return f"{percent}% of {self.num1} is {float(per1)} and " \
                   f"{percent}%  of {self.num2} is {float(per2)}"


class Calculator(Operator):
    def __init__(self, operation, num1=0.0, num2=0.0):
        self.operation = operation
        Operator.__init__(self, num1, num2)
        if operation not in operands:
                print("Enter a valid operation")

    def __str__(self):
        if self.operation in operands:
            return f"You have chosen {self.operation} as an operator"
        else:
            return f"You have entered an invalid operation {self.operation} dosent exist"

    def operate(self):
        if self.operation == "+":
            return self.__add__()
        elif self.operation == "-":
            return self.__sub__()
        elif self.operation == "*" or self.operation == "x":
            return self.__mul__()
        elif self.operation == "/":
            return self.__div__()
        elif self.operation == "**" or self.operation == "^":
            return self.__pow__()
        elif self.operation == "%":
            return self.percentage()
        elif self.operation == "=":
            return self.equal()


if __name__ == "__main__":
    print("You can do the following operations: \n"
          "Addition", "+\n" 
          "Subtraction", "-\n"
          "Division", "/\n"
          "Multiplication", "/\n"
          "Indices", "^\n"
          "Percentage", "%\n"
          "Equals", "=")
    print("To end the operation enter exit as the operation:")

    while True:
        try:
            opcode = str(input("Enter operation: "))
            operands = ["+", "-", "*", "/", "^", "%", "="]
            if opcode.lower() == "exit":
                break
            inp1 = float(input("Enter first number: "))
            inp2 = float(input("Enter second number: "))
            c = Calculator(opcode, inp1, inp2)
            print(c.__str__())
            print(c.operate())
        except ValueError:
            print("First number cannot be left blank")











