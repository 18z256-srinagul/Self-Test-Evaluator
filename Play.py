from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget, ThreeLineIconListItem,ThreeLineAvatarListItem, ImageLeftWidget
import backend
import random as rand
from datetime import datetime


user = []
score=0
start_time,end_time="",""
quesNo=0
Answers=[]
Domain=""
Title=""

QuestionNumbers=[]

class Instructions(Screen):
    pass

class Questions(Screen):
    question_text = ObjectProperty()
    isstart = ObjectProperty()
    ispressed = ObjectProperty()
    opt1 = ObjectProperty()
    opt2 = ObjectProperty()
    opt3 = ObjectProperty()
    opt4 = ObjectProperty()
    currentRightAnswer=""



    def abort_fun(self):
        global score,quesNo
        score = 0
        quesNo = 0

    def startGame(self):
        global start_time
        start_time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        self.isstart.text="Next"
        currentQuestionNumber = self.getQuestions()
        if currentQuestionNumber != -1:
            ques = backend.FetchQandA(currentQuestionNumber)
            self.question_text.text = str(ques[0][0])
            self.currentRightAnswer = str(ques[0][1])

            global QuestionNumbers
            length = len(QuestionNumbers)
            self.options=[]
            self.options.append(currentQuestionNumber)
            r = rand.randint(1,length)
            while len(self.options) != 4 :
                while r in self.options:
                    r = rand.randint(1,length)
                self.options.append(r)

            rand.shuffle(self.options)

            ans = backend.FetchParticularAnswer(self.options[0])
            if ans != -1:
                self.opt1.text = str(ans[0][0])
            else:
                self.opt1.text="Option-1"

            ans = backend.FetchParticularAnswer(self.options[1])
            if ans != -1:
                self.opt2.text = str(ans[0][0])
            else:
                self.opt2.text = "Option-2"

            ans = backend.FetchParticularAnswer(self.options[2])
            if ans != -1:
                self.opt3.text = str(ans[0][0])
            else:
                self.opt3.text = "Option-3"

            ans = backend.FetchParticularAnswer(self.options[3])
            if ans != -1:
                self.opt4.text = str(ans[0][0])
            else:
                self.opt4.text = "Option-4"

        else:
            self.isstart.text = "Finish"

        self.ids.c1.active = False
        self.ids.c2.active = False
        self.ids.c3.active = False
        self.ids.c4.active = False

    def getQuestions(self):
        global quesNo , QuestionNumbers
        if quesNo < len(QuestionNumbers):
            self.questionNo = QuestionNumbers[quesNo]
            quesNo += 1
            return self.questionNo
        else:
            return -1

    def donefunc(self):
        global quesNo
        quesNo -= 1

    def testfunc(self):
        if self.ispressed.text != "":
            global score, Answers
            answer = []
            ansopt = self.options[int(self.ispressed.text)-1]
            opt = list(backend.FetchParticularAnswer(ansopt))[0]
            opt = list(opt)[0]
            ans = opt
            answer.append(opt)
            answer.append(self.currentRightAnswer)
            if self.currentRightAnswer == ans:
                score += 1
                answer.append('1')
            else:
                answer.append('0')

            Answers.append(answer)


class End(Screen):

    def pressed(self,text):
        text = text.split('-->')[0]
        text = text.strip(' ')
        desc = backend.FetchDescription(str(text))
        if desc != -1:
            desc = text+"  ->  "+desc
            btn = MDRectangleFlatButton(text="OK", on_press=self.closes)
            self.dialog = MDDialog(title="Description" , text=str(desc), buttons=[btn],size_hint=(0.7, 1))
            self.dialog.open()


    def closes(self,id):
        self.dialog.dismiss()

    def on_enter(self, *args):
        global end_time
        end_time = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        global score,Answers,quesNo
        try:
            self.score_final = (score/quesNo)*100
        except:
            print('division by zero')
        self.ids.progress.value = self.score_final
        if self.score_final <= 40.0:
            self.ids.progress.color = (1,0,0,1)
        elif self.score_final > 40.0 and self.score_final < 80.0:
            self.ids.progress.color = (1, 1, 0, 1)
        else:
            self.ids.progress.color = (0, 1, 0, 1)
        self.ids.scorepercent.text = "Score: "+str(self.score_final)[:6]+"%"
        for i in Answers:
            string = str(i[0])+" --> Correct Answer: "+str(i[1])
            if str(i[0]) == str(i[1]):
                icon = IconLeftWidget(icon="medal")
            else:
                icon = IconLeftWidget(icon="skull")
            items = TwoLineIconListItem(text=string, secondary_text=str('Score: '+i[2]),on_press= lambda x: self.pressed(x.text))
            items.add_widget(icon)
            self.ids.mylist.add_widget(items)

    def clearall(self):
        global score , start_time, end_time, quesNo, Answers,user,Domain,Title
        s = (score/quesNo)*100
        if backend.InsertScore(user,start_time,end_time,Domain,Title,s) == 0:
            score = 0
            start_time, end_time = "", ""
            quesNo = 0
            Answers.clear()


class Start(Screen):
    pass
class QuestionID(Screen):
    domain = ObjectProperty()
    title = ObjectProperty()
    isvalid = ObjectProperty()

    def validate(self):
        fetch = backend.FetchQuestions(self.domain.text,self.title.text)
        global Domain , Title
        Domain = self.domain.text
        Title = self.title.text
        if fetch != -1:
            self.domain.text=""
            self.title.text=""
            self.isvalid.text="1"

            global QuestionNumbers
            rand.shuffle(fetch)
            QuestionNumbers = fetch
        else:
            self.isvalid.text="0"
            self.popup()

    def popup(self):
        btn = MDRectangleFlatButton(text="OK",on_press = self.closes)
        self.dialog = MDDialog(title="Invalid Entry",text="Please check the domain name and title. No entry in database"
                               ,buttons=[btn],size_hint=(0.7, 1))
        self.dialog.open()

    def closes(self,id):
        self.dialog.dismiss()

class Home(Screen):
    uname = ObjectProperty()
    passw = ObjectProperty()
    isvalid = ObjectProperty()

    def validate(self):
        enteredDetails = backend.FetchLogin(self.uname.text, self.passw.text)
        if self.uname.text != "" and self.passw.text != "" and self.uname.text ==  enteredDetails[0] and self.passw.text == enteredDetails[1]:
            self.isvalid.text = "1"
            user.append(self.uname.text)
            user.append(self.passw.text)
        else:
            self.dialogeBox()
            self.isvalid.text = "0"
        self.uname.text,self.passw.text = "",""

    def dialogeBox(self):
        btn = MDRectangleFlatButton(text="OK", on_press=self.close)
        self.dialog = MDDialog(title='Invalid', text='Please check the credentials you have entered',
                               size_hint=(0.7, 1), buttons=[btn])
        self.dialog.open()

    def close(self,id):
        self.dialog.dismiss()

class Profile(Screen):
    def on_enter(self, *args):
        global user
        profile = backend.FetchLogin(user[0],user[1])
        self.ids.username.text = str(profile[0])
        self.ids.password.text = str(profile[1])

class Scoreboard(Screen):
    def on_enter(self, *args):
        scores = backend.FetchScore()
        prize_count=0
        if scores != -1:
            for i in scores:
                secondText = "Start time : "+i[1]+"             End time: "+i[2]
                if prize_count == 0:
                    image = ImageLeftWidget(source="Images/1.png")
                elif prize_count == 1:
                    image = ImageLeftWidget(source="Images/2.png")
                elif prize_count == 2:
                    image = ImageLeftWidget(source="Images/3.png")
                else:
                    image = ImageLeftWidget(source="Images/4.png")
                items = ThreeLineAvatarListItem(text=str(i[0]), secondary_text=secondText, tertiary_text="Score: "+str(i[3]))
                items.add_widget(image)
                self.ids.mylist.add_widget(items)
                prize_count += 1
        else:
            icon = IconLeftWidget(icon="timer-sand-empty")
            items = ThreeLineIconListItem(text="No games played yet!")
            items.add_widget(icon)
            self.ids.mylist.add_widget(items)

    def clearall(self):
        self.ids.mylist.clear_widgets()


class PlayApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        # self.theme_cls.theme_style="Dark"
        kv = Builder.load_file('play.kv')
        return kv

PlayApp().run()