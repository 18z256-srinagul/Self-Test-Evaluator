import sqlite3 as sql
from datetime import datetime


def initial():
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS User(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT NOT NULL
        );
        """)
    connection.commit()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Questionpalette(
        QuestionpaletteID TEXT PRIMARY KEY,
        CreationTime TEXT,
        QuestionDomain TEXT,
        QuestionTitle TEXT,
        userID INTEGER,
        FOREIGN KEY (userID) REFERENCES User(UserID)
        );
        """)
    connection.commit()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Question(
        QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
        Questionpalette TEXT,
        Question TEXT,
        Answer TEXT,
        Description TEXT,
        FOREIGN KEY (Questionpalette) REFERENCES Questionpalette(QuestionpaletteID)
        );
        """)
    connection.commit()
    c.execute("""
            CREATE TABLE IF NOT EXISTS Score(
            GameID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            questionID INTEGER,
            Username TEXT,
            Starttime TEXT,
            Endtime TEXT,
            QuestionDomain TEXT,
            QuestionTitle TEXT,
            Score INTEGER,
            FOREIGN KEY (userID) REFERENCES User(UserID),
            FOREIGN KEY (questionID) REFERENCES Question(QuestionID)
            );
            """)
    connection.commit()
    connection.close()


def InsertLogin(username, password):
    result=""
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()

    c.execute("SELECT * FROM User WHERE username =:user and password =:pass",{"user":username,"pass":password})
    fetch = c.fetchone()
    if fetch == None:
        c.execute("INSERT INTO User('username','password') values (:user,:pass)",{"user":username,"pass":password})
        connection.commit()
    else:
        result = "alreadyPresent"

    connection.close()
    return result


def FetchLogin(username,password):
    result = ["0","0"]
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    try:
        c.execute("SELECT * FROM User WHERE username=:user and password=:pass",{"user":username,"pass":password})
    except:
        result[0] = result[1] = "-1"
    fetch = c.fetchone()
    if fetch != None:
        result[0] = list(fetch)[1]
        result[1] = list(fetch)[2]
    connection.close()
    return result

def InsertQuestionPalette(questionDomain, questionTitle, user):
    currentTime = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    connection = sql.connect("DATABASE.db")
    c = connection.cursor()

    questionpaletteID = questionDomain.lower() + questionTitle.lower()
    c.execute("SELECT QuestionpaletteID FROM Questionpalette WHERE QuestionpaletteID = :qpid",{"qpid":questionpaletteID})
    fetch = c.fetchall()
    if fetch != None:
        c.execute("SELECT t1.UserID FROM User t1 LEFT JOIN Questionpalette t2 WHERE :user = t1.Username",{"user":user})
        fetch = c.fetchone()
        userID = str(list(fetch)[0])
        try:
            c.execute("INSERT INTO Questionpalette VALUES (:qp,:cr,:qd,:qt,:id)",{"qp":questionpaletteID,"cr":currentTime,"qd":questionDomain,"qt":questionTitle,"id":userID})
        except:
            pass
        connection.commit()
        connection.close()
        return 1
    else:
        connection.close()
        return 0


def InsertQuestion(QuestionDomain , QuestionTitle, Question,Answer,Description):

    connection = sql.connect('DATABASE.db')
    c = connection.cursor()

    c.execute("SELECT Question,Answer,Description FROM Question WHERE Question=:q and Answer=:a and Description=:d",{"q": Question, "a": Answer, "d": Description})
    if len(c.fetchmany()) == 0:
        c.execute(
            "SELECT t1.QuestionpaletteID FROM Questionpalette t1 LEFT JOIN Questionpalette t2 WHERE :d = t1.QuestionDomain and :t = t1.QuestionTitle",
            {"d": QuestionDomain, "t": QuestionTitle})

        ffm = c.fetchmany()
        if len(ffm) != 0:
            qp = ffm[0][0]
            c.execute("INSERT INTO Question(Questionpalette,Question,Answer,Description) VALUES (:qp,:q,:a,:d)",
                      {"qp": qp, "q": Question, "a": Answer, "d": Description})
            connection.commit()
            connection.close()
            return 1
        else:
            connection.close()
            return 0

    else:
        connection.close()
        return -1

def profile(username):
    connection = sql.connect('DATABASE.db')
    conn = connection.cursor()
    try:
        conn.execute("SELECT name,username,email FROM users WHERE username = (:username)", {"username": username})
    except:
        return 'No data found!'
    connection.commit()
    details = conn.fetchall()
    connection.close()

    if details == None or details == []:
        return 'No data found!'
    else:
        details = list(details)
        return details

def FetchQuestions(qd,qt):
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("SELECT QuestionpaletteID from QuestionPalette WHERE QuestionDomain = :qd and QuestionTitle = :qt",{"qd":qd,"qt":qt})
    fetch = c.fetchone()
    if fetch == None:
        connection.close()
        return -1
    qpi = fetch[0]

    c.execute("SELECT QuestionID FROM Question WHERE Questionpalette = :qp",{"qp":qpi})
    questions = []
    fetch = c.fetchall()
    if fetch == -1:
        connection.close()
        return -1
    for i in fetch:
        questions.append(list(i)[0])
    connection.close()
    return questions

def FetchQandA(QuestionNumber):
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("SELECT Question,Answer,Description from Question WHERE QuestionID = :qd",{"qd":QuestionNumber})
    fetch = c.fetchall()
    if fetch == None or len(fetch) == 0:
        connection.close()
        return -1
    question = []

    for q in fetch:
        temp=[]
        temp.append(q[0])
        temp.append(q[1])
        temp.append(q[2])
        question.append((temp))
    connection.close()
    return question

def FetchParticularAnswer(AnswerNumber):
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("SELECT Answer from Question WHERE QuestionID = :qd",{"qd":AnswerNumber})
    fetch = c.fetchall()
    if fetch == None or len(fetch) == 0:
        connection.close()
        return -1
    question = []
    for q in fetch:
        question.append(q)
    connection.close()
    return question

def InsertScore(user,start_time,end_time,Domain,Title,score):
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    try:
        c.execute("SELECT UserID FROM User WHERE username = :u AND password = :p",{"u":user[0],"p":user[1]})
    except:
        print('insert exception1')

    fetch = c.fetchone()
    if fetch == None:
        connection.close()
        return -1
    else:
        fetch = list(fetch)[0]
        userid = fetch

    try:
        c.execute("SELECT QuestionpaletteID FROM Questionpalette WHERE QuestionDomain = :d AND QuestionTitle = :t",{"d":Domain,"t":Title})
    except:
        print('insert exception2')

    fetch = c.fetchone()
    if fetch == None:
        connection.close()
        return -1
    else:
        fetch = list(fetch)[0]
        questionpaletteid = fetch
    username = user[0]
    c.execute("INSERT INTO Score(userID,questionID,Username,Starttime,Endtime,QuestionDomain,QuestionTitle,Score) "
              "VALUES (:uid,:qid,:user,:start,:end,:qd,:qt,:score)",
              {"uid": userid, "qid": questionpaletteid, "user": username, "start": start_time, "end":end_time,"qd":Domain,"qt":Title,"score":score})
    connection.commit()
    connection.close()
    return 0

def FetchScore():
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("SELECT Username , Starttime , Endtime , Score FROM Score ORDER BY Score Desc")

    fetch = c.fetchall()

    if fetch == None or len(fetch) == 0:
        connection.close()
        return -1
    result=[]
    for i in fetch:
        result.append(list(i))
    connection.close()
    return result

def FetchDescription(answer):
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("SELECT Description FROM Question WHERE Answer = :ans",{"ans":str(answer)})

    fetch = c.fetchone()
    if fetch == None or len(fetch) == 0:
        connection.close()
        return -1
    fetch = list(fetch)[0]
    connection.close()
    return fetch

def test():
    connection = sql.connect('DATABASE.db')
    c = connection.cursor()
    c.execute("SELECT * FROM Score")
    for i in c.fetchall():
        print(i)
    connection.close()