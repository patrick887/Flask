import sqlite3


class basicSQL:
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db)

    def connect(self):
        self.conn = sqlite3.connect(self.db)

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def execute(self, string, fetch=False):
        self.connect()
        cur = self.cursor()
        cur.execute(string)
        if fetch:
            value = cur.fetchone()
            self.close()
            return value
        self.close()


class User(basicSQL):
    def __init__(self):
        basicSQL.__init__(self, "Users.db")

    def createTableUser(self):
        create = """CREATE TABLE IF NOT EXISTS 
                    user(
                    CandidateNumber CHAR(4) PRIMARY KEY, 
                    Username VARCHAR(20), 
                    Password VARCHAR(20), 
                    Teacher VARCHAR(20)
                    )"""
        super().execute(create)

    def checkUser(self, Username, Password):
        query = """SELECT Username, Password 
                    FROM user WHERE Username = '{}' 
                    AND Password = '{}'""".format(Username, Password)
        check = super().execute(query, True)
        return check

    def addUser(self, CandidateNumber, Username, Password):
        check = self.checkUser(Username, Password)
        if check is None:
            insert = """INSERT INTO user 
                        VALUES('{}', '{}', '{}')""".format(CandidateNumber, Username, Password)
            super().execute(insert)
            return 1
        return 0

    def updatePassword(self, Password, CandidateNumber):
        edit = """UPDATE user SET Password = '{}' WHERE CandidateNumber = '{}'""".format(Password, CandidateNumber)
        super().execute(edit)

    def deleteUser(self, CandidateNumber):
        delete = """DELETE FROMM user WHERE CandidateNumber = '{}'""".format(CandidateNumber)
        super().execute(delete)


class TestResult(basicSQL):
    def __init__(self):
        super().__init__("Users.db")

    def createTestResult(self):
        create = """CREATE TABLE IF NOT EXISTS 
                    TestResult(
                    CandidateNumber CHAR(4), 
                    TestID CHAR(10), 
                    Mark FLOAT, 
                    Grade VARCHAR(1), 
                    Topic VARCHAR(15), 
                    PRIMARY KEY(CandidateNumber, TestID))"""
        super().execute(create)

    def addResult(self, CandidateNumber, TestID, Mark, Grade, Topic):
        insert = """INSERT INTO TestResult 
                    VALUES('{}', '{}', '{}', '{}', '{}')""".format(CandidateNumber, TestID, Mark, Grade, Topic)
        super().execute(insert)

    def getResult(self, TestID):
        query = """SELECT Username, Grade 
                    FROM user, TestResult 
                    WHERE user.CandidateNumber = TestResult.CandidateNumber 
                    AND TestResult.TestID = {}""".format(TestID)
        value = super().execute(query, True)
        return value

    def avgResult(self, CandidateNumber):
        avg = """SELECT AVG(Mark) FROM TestResult WHERE CandidateNumber = '{}'""".format(CandidateNumber)
        value = super().execute(avg, True)
        return value


class TestBoundary(basicSQL):
    def __init__(self):
        super().__init__("User.db")

    def createTableBoundary(self):
        create = """CREATE TABLE IF NOT EXISTS 
                    TestBoundary(
                    TestID CHAR(10) PRIMARY KEY, 
                    A FLOAT, 
                    B FLOAT, 
                    C FLOAT, 
                    Pass FLOAT)"""
        super().execute(create)

    def addTestBoundary(self, TestID, A, B, C, Pass):
        insert = """INSERT INTO TestBoundary 
                    VALUES('{}', '{}', '{}', '{}', '{}')""".format(TestID, A, B, C, Pass)
        super().execute(insert)

    def getTestBoundary(self, TestID):
        query = """SELECT * FROM TestBoundary WHERE TestID = '[]'""".format(TestID)
        value = super().execute(query, True)
        return value


class TopicTracker(basicSQL):
    def __init__(self):
        super().__init__("Tracker.db")

    def createTableTopicTracker(self):
        create = """CREATE TABLE IF NOT EXISTS TopicTracker(Topic CHAR(11), Counter INTEGER)"""
        super().execute(create)

    def firstRun(self):
        input = [
            ["Binomial", 0],
            ["Poisson", 0],
            ["Continuous", 0],
            ["Discrete", 0],
            ["Normal", 0],
            ["Rectangular", 0]
        ]
        for i in range(len(input)):
            insert = "INSERT INTO TopicTracker VALUES('{}', '{}')".format(input[i][0], input[i][1])
            super().execute(insert)

    def updateTopic(self, Topic):
        value = self.getCurrentValue(Topic)
        update = """UPDATE TopicTracker SET Count = '{}' WHERE Topic = '{}'""".format(value + 1, Topic)
        super().execute(update)

    def getCurrentValue(self, Topic):
        query = """SELECT Count FROM TopicTracker WHERE Topic = '{}'""".format(Topic)
        value = super().execute(query, True)
        return int(value[0])


class TestQuestions(basicSQL):
    def __init__(self):
        super().__init__("Test.db")

    def createTableTestQuestions(self):
        create = """CREATE TABLE IF NOT EXISTS 
                    TestQuestion(
                    TestID CHAR(10), 
                    QuestionNumber INTEGER, 
                    Question VARCHAR(255),
                    PRIMARY KEY(TestID, QuestionNumber))"""
        super().execute(create)

    def getQuestion(self, TestID, QuestionNumber):
        query = """SELECT Question FROM Test WHERE TestID = '{}' AND QuestionNumber = '{}'""".format(TestID, QuestionNumber)
        question = super().execute(query, True)
        return question


class TestAnswers(basicSQL):
    def __init__(self):
        super().__init__("Test.db")

    def createTableTestAnswers(self):
        create = """CREATE TABLE IF NOT EXISTS 
                    TestAnswer(
                    TestID CHAR(10), 
                    QuestionNumber INTEGER, 
                    Answer VARCHAR(100),
                    PRIMARY KEY(TestID, QuestionNumber))"""
        super().execute(create)

    def getAnswer(self, TestID, QuestionNumber):
        query = """SELECT Answer FROM Test WHERE TestID = '{}' AND QuestionNumber = '{}'""".format(TestID, QuestionNumber)
        answer = super().execute(query, True)
        return answer


class Teacher(basicSQL):
    def __init__(self):
        super().__init__("Teacher.db")

    def execute(self, string, fetch=False):
        self.connect()
        cur = self.cursor()
        cur.execute(string)
        if fetch:
            value = cur.fetchall()
            self.close()
            return value
        self.close()

    def createTableTeacher(self):
        create = """CREATE TABLE IF NOT EXISTS Teacher(CandidateNumber PRIMARY KEY CHAR(4), Username VARCHAR(20))"""
        super().execute(create)

    def getUser(self, Username):
        query = """SELECT Username FROM Teacher""".format(Username)
        value = super().execute(query, True)
        return value


