from re import split
from threading import Thread
from queue import PriorityQueue
from flask import message_flashed

class BasicMaths:
    @staticmethod
    def integration(equation, upper, lower):
        signs = []
        upper_value = []
        lower_value = []
        if equation[0] != "-":
            signs.append("+")
        for i in equation:
            if i == "+" or i == "-":
                signs.append(i)
        if equation[0] == "-":
            equation = equation[1:]
        equation = split("[+-]", equation)
        for part in equation:
            if "x" not in part:
                upper_value.append(float(part) * upper)
                lower_value.append(float(part) * lower)
            if "x" in part:
                if "^" in part:
                    power = split("[x^]", part)
                    newpower = float(power[-1]) + 1
                    if power[0] != "":
                        upper_value.append(float(power[0])/newpower * upper ** newpower)
                        lower_value.append(float(power[0])/newpower * lower ** newpower)
                    else:
                        upper_value.append(1/newpower * upper ** newpower)
                        lower_value.append(1/newpower * lower ** newpower)
                else:
                    coef_x = split("[x]", part)
                    upper_value.append(float(coef_x[0])/2 * upper ** 2)
                    lower_value.append(float(coef_x[0])/2 * lower ** 2)

        for sign in range(len(signs)):
            if signs[sign] == "-":
                upper_value[sign] = upper_value[sign] * -1
                lower_value[sign] = lower_value[sign] * -1
        final_lower_value = 0
        final_upper_value = 0
        for i in range(len(upper_value)):
            final_upper_value = final_upper_value + upper_value[i]
            final_lower_value = final_lower_value + lower_value[i]
        return final_upper_value - final_lower_value

    @staticmethod
    def expand_brackets(fx):
        fx = split("[()]", fx)
        print(fx)

    def Factorial(self, n):
        if n == 1:
            return n
        elif n == 0:
            return 1
        else:
            return n * self.Factorial(n - 1)

    def Euluers(self):
        e = 0
        for i in range(0, 100):
            e = 1 / self.Factorial(i) + e
        return e

    @staticmethod
    def Pi():
        count = 0
        pi = 3
        for i in range(2, 1000, 2):
            count += 1
            if count % 2 == 1:
                pi = pi + 4 / (i * (i + 1) * (i + 2))
            else:
                pi = pi - 4 / (i * (i + 1) * (i + 2))
        return pi


# Everything to do with rectangular
class Rectangular:
    def __init__(self, a, b):
        try:
            self.a = float(a)
            self.b = float(b)
        except ValueError:
            message_flashed("please input the correct values")

    def expectation(self):
        try:
            return (self.a + self.b)/2
        except ValueError:
            return False

    def variance(self):
        return 1/12 * (self.a ** 2 - 2 * self.b * self.a + self.a ** 2)


# Everything to do with Binomial
class Binomial(BasicMaths):
    def __init__(self, n, p, r=0):
        super().__init__()
        self.n = float(n)
        self.p = float(p)
        self.q = 1 - self.p
        self.r = float(r)

    def expectation(self):
        return self.n * self.p

    def variance(self):
        return self.n * self.p * self.q

    def prob_dist(self):
        ncr = self.Factorial(self.n) / (self.Factorial(self.n - self.r) * self.Factorial(self.r))
        return ncr * (self.p ** self.r) * (self.q ** (self.n - self.r))

    def prob_dist_range(self, lower, upper):
        value = 0
        for i in range(lower, upper+1):
            self.r = i
            value = self.prob_dist() + value
        return value


# Everything to do with Poisson
class Poisson(BasicMaths):
    def __init__(self, mean, no_events):
        super().__init__()
        self.mean = float(mean)
        self.no_events = int(no_events)

    def prob_dist(self):
        return ((self.no_events ** self.mean) / self.Factorial(self.mean)) * self.Euluers() ** (-self.no_events)

    def prob_dist_range(self, lower, upper):
        value = 0
        for i in range(lower, upper):
            self.no_events = i
            value = self.prob_dist() + value
        return value


# Everything to do with Continuous Random Variable
class Continuous(BasicMaths):
    def __init__(self, fx, upper, lower):
        BasicMaths.__init__(self)
        self.fx = fx
        self.upper = float(upper)
        self.lower = float(lower)

    def addx(self, fx=""):
        signs = []
        if fx == "":
            fx = self.fx
        if fx[0] != "-":
            signs.append("+")
        for i in fx:
            if i == "+" or i == "-":
                signs.append(i)
        if fx[0] == "-":
            fx = fx[1:]
        final_equation = []
        equation = split("[+-]", fx)
        for part in equation:
            if "x" not in part:
                final_equation.append(part + "x")
            if "x" in part:
                if "^" in part:
                    power = split("[x^]", part)
                    newpower = int(power[-1]) + 1
                    final_equation.append(power[0] + "x^" + str(newpower))
                else:
                    coef_x = split("[x]", part)
                    final_equation.append(coef_x[0] + "x^2")
        fx = ""
        try:
            for sign in range(len(signs)):
                fx = fx + "{}{}".format(signs[sign], final_equation[sign])
        except IndexError:
            pass
        if fx[0] == "+":
            fx = fx[1:]
        return fx

    def expectation(self, my_queue=None):
        fx = Continuous.addx(self)
        if my_queue is None:
            return super().integration(fx, self.upper, self.lower)
        else:
            my_queue.put((1, super().integration(fx, self.upper, self.lower)))

    def expectation_squared(self, my_queue=None):
        fx = Continuous.addx(self)
        fx = Continuous.addx(self, fx)
        if my_queue is None:
            return super().integration(fx, self.upper, self.lower)
        else:
            my_queue.put((2, super().integration(fx, self.upper, self.lower)))

    def variance(self):
        my_queue = PriorityQueue()
        thread_ex = Thread(target=self.expectation(my_queue))
        thread_sqrd = Thread(target=self.expectation_squared(my_queue))
        thread_ex.start()
        thread_sqrd.start()
        thread_sqrd.join()
        thread_ex.join()
        ex = my_queue.get()
        ex_sqrd = my_queue.get()
        return ex_sqrd - ex ** 2


# Everything to do with Discrete
class Discrete:
    def __init__(self, pxx, x):
        self.x = x
        self.pxx = pxx

    def expectation(self, my_queue=None):
        x = self.x.split()
        pxx = self.pxx.split()
        if len(x) == len(pxx):
            expect = 0
            for i in range(len(x)):
                expect = expect + float(x[i]) * float(pxx[i])
            if my_queue is None:
                return expect
            else:
                my_queue.put((1, expect))

    def expectation_squared(self, my_queue=None):
        x = self.x.split()
        pxx = self.pxx.split()
        if len(x) == len(pxx):
            sqrd = 0
            for i in range(len(x)):
                sqrd = sqrd + float(x[i]) ** 2 * float(pxx[i])
            if my_queue is None:
                return sqrd
            else:
                my_queue.put((2, sqrd))

    def variance(self):
        my_queue = PriorityQueue()
        thread_ex = Thread(target=self.expectation(my_queue))
        thread_sqrd = Thread(target=self.expectation_squared(my_queue))
        thread_ex.start()
        thread_sqrd.start()
        thread_sqrd.join()
        thread_ex.join()
        ex = my_queue.get()
        ex_sqrd = my_queue.get()
        return ex_sqrd - ex ** 2


