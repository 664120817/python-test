from PyQt5.Qt import *
from resource.register import Ui_Form


class RegisterPane(QWidget, Ui_Form):

    exit_signal = pyqtSignal()
    register_account_pwd_signal=pyqtSignal(str,str)
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)

        self.animation_targets = [self.about_menue_btn, self.reset_menue_btn, self.exit_menue_btn]

        self.animation_targets_pos = [target.pos() for target in self.animation_targets]

    def show_hide_menue(self, checked):
        print("显示和隐藏", checked)

        animation_group = QSequentialAnimationGroup(self)
        for idx, target in enumerate(self.animation_targets):

              animation = QPropertyAnimation()

              animation.setTargetObject(target)

              animation.setPropertyName(b"pos")
              if not checked:
                 animation.setStartValue(self.main_menue_btn.pos())
                 animation.setEndValue(self.animation_targets_pos[idx])

              else:
                  animation.setEndValue(self.main_menue_btn.pos())
                  animation.setStartValue(self.animation_targets_pos[idx])


              animation.setDuration(100)
              animation.setEasingCurve(QEasingCurve.InOutBounce)
              animation_group.addAnimation(animation)
        animation_group.start(QAbstractAnimation.DeleteWhenStopped)

    def about_lk(self):
        print("关于")
        QMessageBox.about(self,"百度","https://www.baidu.com/")

    def reset(self):
        print("重置")
        self.account_le.clear()
        self.password_le.clear()
        self.confirm_pwd_le.clear()

    def exit_pane(self):
        self.exit_signal.emit()

    def check_register(self):
        account_txt = self.account_le.text()
        password_txt = self.password_le.text()
        self.register_account_pwd_signal.emit(account_txt,password_txt)

    def enable_register_btn(self):
        print("判定")

        account_txt = self.account_le.text()
        password_txt= self.password_le.text()
        cp_txt = self.confirm_pwd_le.text()
        if len(account_txt )>0 and len(password_txt )>0 and len( cp_txt)>0 and password_txt == cp_txt:
            self.register_btn.setEnabled(True)
        else:
            self.register_btn.setEnabled(False)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = RegisterPane()
    window.exit_signal.connect(lambda:print("退出"))
    window.register_account_pwd_signal.connect(lambda a,p:print(a,p))
    window.show()

    sys.exit(app.exec_())
