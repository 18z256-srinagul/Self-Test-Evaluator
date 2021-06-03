from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
import backend

up=["",""]
qp = ["",""]
class Login(Screen):
    uname = ObjectProperty()
    upass = ObjectProperty()
    isUser = ObjectProperty()

    def Validate(self):
        enteredDetails = backend.FetchLogin(self.uname.text,self.upass.text)

        if self.uname.text != "" and self.upass.text != "" and self.uname.text ==  enteredDetails[0] and self.upass.text == enteredDetails[1] :
            self.isUser.text = "1"
            up[0] = self.uname.text
            up[1] = self.upass.text
        else:
            self.isUser.text="0"
        self.uname.text=""
        self.upass.text=""


class Signup(Screen):
    uname = ObjectProperty()
    upass = ObjectProperty()

    def Insert(self):
        if self.uname.text != "" and self.upass.text != "":
            backend.InsertLogin(self.uname.text, self.upass.text)


class FirstScreen(Screen):
    pass

class Instructions(Screen):
    pass

class DomainScreen(Screen):
    domain = ObjectProperty()
    title = ObjectProperty()
    result = ObjectProperty()

    def EnterDomain(self):
        qp[0] = self.domain.text
        qp[1] = self.title.text

        if self.domain.text != "" and self.title.text != "":
            res = backend.InsertQuestionPalette(self.domain.text,self.title.text,up[0])
            if res == 1:
                self.domain.text=""
                self.title.text=""
                self.result.text="1"
            else:
                self.result.text="0"


class Questions(Screen):

    ques = ObjectProperty()
    ans = ObjectProperty()
    desc = ObjectProperty()
    cont=ObjectProperty()

    def validate(self):
        if self.ques.text != "" and self.ans.text != "" and self.desc.text != "":
            res = backend.InsertQuestion(qp[0],qp[1],self.ques.text,self.ans.text,self.desc.text)
            if res == 1:
                self.cont.text = "1"
            else:
                self.cont.text = "0"
            self.ques.text = ""
            self.ans.text = ""
            self.desc.text = ""

class Error(Screen):
    pass

class End(Screen):
    pass

class Arrival(ScreenManager):
    pass

kv = Builder.load_file("questionenter.kv")

class QuestionenterApp(App):
    def build(self):
        return kv

backend.initial()
QuestionenterApp().run()