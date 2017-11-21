from re import split


def Factorial(n):
    if n == 1:
        return n
    elif n == 0:
        return 1
    else:
        return n * Factorial(n - 1)


def Euluers():
    e = 0
    for i in range(0, 100):
        e = 1 / Factorial(i) + e
    return e


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
        self.a = float(a)
        self.b = float(b)

    def expectation(self):
        return (self.a + self.b)/2

    def variance(self):
        return 1/12 * (self.a ** 2 - 2 * self.b * self.a + self.a ** 2)


# Everything to do with Binomial
class Binomial:
    def __init__(self, n, p, r=0):
        self.n = float(n)
        self.p = float(p)
        self.q = 1 - p
        self.r = float(r)

    def expectation(self):
        return self.n * self.p

    def variance(self):
        return self.n * self.p * self.q

    def prod_dist(self):
        ncr = Factorial(self.n) / (Factorial(self.n - self.r) * Factorial(self.r))
        return ncr * (self.p ** self.r) * (self.q ** (self.n - self.r))

    def prob_dist_range(self, lower, upper):
        pass


# Everything to do with Poisson
class Poisson:
    def __init__(self, mean, no_events):
        self.mean = float(mean)
        self.no_events = float(no_events)

    def prob_dist(self):
        return ((self.no_events ** self.mean) / Factorial(self.mean)) * Euluers() ** (-self.no_events)

    def prob_dist_range(self, lower, upper):
        pass


# Everything to do with Continuous Random Variable
class Continuous:
    def __init__(self, fx, upper, lower):
        self.fx = fx
        self.upper = upper
        self.lower = lower
        self.signs = []

    def addx(self):
        if self.fx[0] != "-":
            self.signs.append("+")
        for i in self.fx:
            if i == "+" or i == "-":
                self.signs.append(i)
        if self.fx[0] == "-":
            self.fx = self.fx[1:]
        final_equation = []
        equation = split("[+-]", self.fx)
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
        self.fx = ""
        for sign in range(len(self.signs)):
            self.fx = self.fx + "{}{}".format(self.signs[sign], final_equation[sign])
        if self.fx[0] == "+":
            self.fx = self.fx[1:]
        return self.fx

    def expectation(self):
        self.fx = Continuous.addx(self)
        return integration(self.fx, self.upper, self.lower)

    def variance(self):
        self.fx = Continuous.addx(self)
        self.fx = Continuous.addx(self)
        return integration(self.fx, self.upper, self.lower)


# Everything to do with Discrete
class Discrete:
    def __init__(self, pxx, x):
        self.x = x
        self.pxx = pxx

    def expectation(self):
        self.x = self.x.split()
        self.pxx = self.pxx.split()
        if len(self.x) == len(self.pxx):
            expect = 0
            for i in range(len(self.x)):
                expect = expect + float(self.x[i]) * float(self.pxx[i])
            return expect

    def variance(self):
        self.x = self.x.split()
        self.pxx = self.pxx.split()
        if len(self.x) == len(self.pxx):
            var = 0
            for i in range(len(self.x)):
                var = var + float(self.x[i]) ** 2 * float(self.pxx[i])
            return var


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
                newpower = int(power[-1]) + 1
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
