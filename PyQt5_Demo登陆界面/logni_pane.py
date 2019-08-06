from PyQt5.Qt import *
from resource.login import Ui_Form


class LogniPane(QWidget, Ui_Form):

    show_register_pane_signal = pyqtSignal()
    check_login_signal = pyqtSignal(str,str)
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        movie=QMovie(":/login/images/logni_top_bg1.gif")
        movie.setScaledSize(QSize(500,232))
        self.login_top_bg_label.setMovie(movie)
        movie.start()
    def show_register_pane(self):
        print("弹出注册界面")
        self.show_register_pane_signal.emit()

    def open_qq_link(self):
        link= "http://shang.qq.com/wpa/qunwpa?idkey=20e13047848678d21217f52d2f736ccc976da1127da862390ccbe1adc3c6635b"
        QDesktopServices.openUrl(QUrl(link))

    def enable_login_btn(self):
         QComboBox
         account=self.account_cb.currentText()
         pwd=self.pwd_le.text()
         print(account,pwd)
         if len(account)>0 and len(pwd)>0:
             self.login_btn.setEnabled(True)

         else:
             self.login_btn.setEnabled(False)

    def check_login(self):
        account = self.account_cb.currentText()
        pwd = self.pwd_le.text()
        self.check_login_signal.emit(account,pwd)

    def auto_login(self,checked):
        print("自动登录",checked)
        if checked:
            self.remember_pwd_cb.setChecked(True)
    def remember_pwd(self, checked):
        print("记住密码", checked)
        if not checked:
            self.auto_login_cb.setChecked(False)

    def show_error_animation(self):
        animation =QPropertyAnimation(self)
        animation.setTargetObject(self.login_bottom)
        animation.setPropertyName(b"pos")
        animation.setKeyValueAt(0,self.login_bottom.pos())
        animation.setKeyValueAt(0.2, self.login_bottom.pos()+QPoint(15,0))
        animation.setKeyValueAt(0.5, self.login_bottom.pos())
        animation.setKeyValueAt(0.7, self.login_bottom.pos()+QPoint(-15,0))
        animation.setKeyValueAt(1, self.login_bottom.pos())
        animation.setDuration(200)
        animation.setLoopCount(3)
        animation.start(QAbstractAnimation.DeleteWhenStopped)
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = LogniPane()
    window.show()

    sys.exit(app.exec_())