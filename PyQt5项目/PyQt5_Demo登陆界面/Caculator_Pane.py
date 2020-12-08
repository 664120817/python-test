from PyQt5.Qt import *
from resource.caculator import Ui_Form

class  Caculator(QObject):

    show_content = pyqtSignal(str)
    def __init__(self,parent):
        super().__init__(parent)
       # self.setParent(parent)
       #数字键位num 运算符 operator
        self.key_models =[]
    def caculate(self):
        if len(self.key_models) > 0 and self.key_models[-1]["role"] =="operator":
            self.key_models.pop(-1)
        expression =""
        for model  in  self.key_models:
            expression += model["title"]

        result=eval(expression)
        return  result
        print(result)


    def parse_key_model(self,key_model):
       # print(key_model)
        if key_model["role"] =="clear":
            print("清空所有内容")
            self.key_models = []
            self.show_content.emit("0.0")
            return None
        if key_model["role"] =="caculate":
            print("计算所有内容")
            result=self.caculate()
            self.show_content.emit(str(result))
            return None
        if len(self.key_models) ==0:
           if key_model["role"] =="num":

               if key_model["title"] ==".":
                   key_model["title"] = "0."
               self.key_models.append(key_model)
               self.show_content.emit(self.key_models[-1]["title"])
           return None
        if key_model["title"] in ("%","+/-","-"):
            if self.key_models[-1]["role"] != "num":
                return  None
            else:
                if key_model["title"] =="%":
                    self.key_models[-1]["title"] = str(float(self.key_models[-1] ["title"]) /100)
                elif key_model["title"] == "+/-":
                    self.key_models[-1]["title"] = str(float(self.key_models[-1]["title"]) * -1)
                self.show_content.emit(self.key_models[-1]["title"])
            return None

        if key_model["role"] ==self.key_models[-1]["role"]:
            if key_model['role'] == "num":

                if key_model["title"] == "." and self.key_models[-1]["title"].__contains__("."):
                    return None
                if self.key_models[-1]["title"] != "0":
                   self.key_models[-1]["title"] += key_model["title"]
                else:
                    self.key_models[-1]["title"] = key_model["title"]
                self.show_content.emit(self.key_models[-1]["title"])

            if key_model["role"] =="operator":
                self.key_models[-1]["title"] = key_model["title"]
                self.show_content.emit(str(self.caculate()))

        else:
            if key_model["title"] in (".","%","+/-"):
                return None
            if key_model["role"] =="num":
                self.show_content.emit(key_model["title"])
            elif key_model["role"] =="operator":
                self.show_content.emit(str(self.caculate()))

            self.key_models.append(key_model)

        print(self.key_models)


class CaculatorPane(QWidget, Ui_Form):

    show_register_pane_signal = pyqtSignal()
    check_login_signal = pyqtSignal(str,str)

    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.caculator = Caculator(self)
        self.caculator.show_content.connect(self.show_content)
    def show_content(self,content):
        self.lineEdit.setText(content)

    def get_key(self,title,role):
#       print(title,role)
        self.caculator.parse_key_model({"title":title,"role":role})
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = CaculatorPane()
    window.show()

    sys.exit(app.exec_())