from flask import Flask
from flask import request, redirect, url_for, render_template
import Mysql
import Maths
from threading import Thread

app = Flask(__name__)

# prepare all the threads for creating each table
createUser = Mysql.User()
t1 = Thread(target=createUser.createTableUser())
createTracker = Mysql.TopicTracker()
t2 = Thread(target=createTracker.createTableTopicTracker())
createTest = Mysql.TestQuestions()
t3 = Thread(target=createTest.createTableTestQuestions())
createBound = Mysql.TestBoundary()
t4 = Thread(target=createBound.createTableBoundary())


# beginning page
@app.route('/')
def index():
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    return render_template("Home.html")


@app.route('/Register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return checkRegister(request.form['Username'], request.form['Password'], request.form['confirmPassword'], request.form['cand'])
    else:
        return render_template("Register.html")


@app.route('/Home')
def logged_in():
    return render_template("Home login.html")


@app.route('/Login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return checkLogin(request.form['Username'], request.form['Password'])
    else:
        return render_template("Login.html")


@app.route('/Poisson', methods=['GET', 'POST'])
def poisson():
    if request.method == "POST":
        value = poissonProb(request.form['average'], request.form['variable'])
        return render_template("Poisson.html", value=value, averageValue=request.form['average'], variableValue=request.form['variable'])
    else:
        return render_template("Poisson.html", averageValue="Average rate", variableValue="Random Variable")


@app.route('/Binomial', methods=['GET', 'POST'])
def binomial():
    if request.method == "POST":
        value = binomialEx(request.form['event'], request.form['number'], request.form['prob'])
        return render_template("Binomial.html", value=value)
    else:
        return render_template("binomial.html")


@app.route('/Discrete', methods=['GET', 'POST'])
def discrete():
    if request.method == "POST":
        X = request.form['1'] + " " + request.form['2'] + " " + request.form['3'] + " " + request.form['4'] + " " + \
            request.form['5'] + " " + request.form['6']
        PXx = request.form['1x'] + " " + request.form['2x'] + " " + request.form['3x'] + " " + request.form[
            '4x'] + " " + request.form['5x'] + " " + request.form['6x']
        value = discreteEx(X, PXx)
        return render_template("Discrete.html", value=value)
    else:
        return render_template("Discrete.html")


@app.route('/Normal')
def normal():
    return render_template("Normal.html")


@app.route('/Rectangular', methods=['GET', 'POST'])
def rectangular():
    if request.method == 'POST':
        value = rectangularEx(request.form['upper'], request.form['lower'])
        return render_template("Rectangular.html", value=value)
    else:
        return render_template("Rectangular.html")


@app.route('/Continuous', methods=['GET', 'POST'])
def continuous():
    if request.method == "POST":
        value = continuousEx(request.form['equation'], request.form['upper'], request.form['lower'])
        return render_template("Continuous.html", value=value)
    else:
        return render_template("Continuous.html")


@app.route('/Test')
def test():
    return render_template("Test.html")


@app.route('/BinomialVar', methods=["POST", "GET"])
def binomialVar():
    if request.method == "POST":
        value = binomialVarx(request.form["event"], request.form["number"], request.form["prob"])
        return render_template("binomialVar.html", value=value)
    else:
        return render_template("binomialVar.html")


@app.route('/ContinuousVar', methods=['GET', 'POST'])
def continuousVar():
    if request.method == "POST":
        value = continuousVarx(request.form['equation'], request.form['upper'], request.form['lower'])
        return render_template("ContinuousVar.html", value=value)
    else:
        return render_template("ContinuousVar.html")


@app.route('/RectangularVar', methods=['GET', 'POST'])
def rectangularVar():
    if request.method == 'POST':
        value = rectangularVarx(request.form['upper'], request.form['lower'])
        return render_template("RectangularVar.html", value=value)
    else:
        return render_template("RectangularVar.html")


@app.route('/DiscreteVar', methods=['GET', 'POST'])
def discreteVar():
    if request.method == "POST":
        X = request.form['1'] + " " + request.form['2'] + " " + request.form['3'] + " " + request.form['4'] + " " + \
            request.form['5'] + " " + request.form['6']
        PXx = request.form['1x'] + " " + request.form['2x'] + " " + request.form['3x'] + " " + request.form[
            '4x'] + " " + request.form['5x'] + " " + request.form['6x']
        value = discreteVarx(X, PXx)
        return render_template("DiscreteVar.html", value=value)
    else:
        return render_template("DiscreteVar.html")


@app.route('/Further knowledge')
def further():
    return render_template("Further knowledge.html")


def checkRegister(username, password, confirm, candidateNumber):
    candidateNumber = int(candidateNumber)
    if password == confirm:
        user = Mysql.User()
        check = user.addUser(candidateNumber, username, password)
        if check == 1:
            return redirect(url_for('logged_in'))
        else:
            return redirect(url_for("register"))
    else:
        return redirect(url_for("register"))


def checkLogin(username, password):
    checker = Mysql.User()
    check = checker.checkUser(username, password)
    if check is None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for("logged_in"))


def poissonProb(average, variable):
    prob = Maths.Poisson(average, variable)
    return prob.prob_dist()


def binomialEx(event, number, prob):
    ex = Maths.Binomial(number, prob, event)
    return ex.expectation()


def discreteEx(X, PXx):
    ex = Maths.Discrete(PXx, X)
    return ex.expectation()


def rectangularEx(upper, lower):
    ex = Maths.Rectangular(lower, upper)
    return ex.expectation()


def continuousEx(equation, upper, lower):
    ex = Maths.Continuous(equation, upper, lower)
    return ex.expectation()


def binomialVarx(event, number, prob):
    varx = Maths.Binomial(number, prob, event)
    return varx.variance()


def continuousVarx(equation, upper, lower):
    varx = Maths.Continuous(equation, upper, lower)
    return varx.variance()


def rectangularVarx(upper, lower):
    varx = Maths.Rectangular(lower, upper)
    return varx.variance()


def discreteVarx(X, PXx):
    varx = Maths.Discrete(PXx, X)
    return varx.variance()


if __name__ == "__main__":
    app.debug = True
    app.run()