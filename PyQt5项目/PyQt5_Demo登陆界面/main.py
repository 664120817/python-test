from logni_pane import LogniPane
from Register_Pane import RegisterPane
from Caculator_Pane import CaculatorPane
from PyQt5.Qt import *

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    login_pane = LogniPane()
    register_pane = RegisterPane(login_pane)
    register_pane.move(0, login_pane.height())
    register_pane.show()
    caculator_pane = CaculatorPane()


    def exit_register_pane():
        animation = QPropertyAnimation(register_pane)
        animation.setTargetObject(register_pane)
        animation.setPropertyName(b"pos")
        animation.setStartValue(QPoint(0, 0))
        animation.setEndValue(QPoint(login_pane.width(), 0))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.InBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)


    def show_register_pane():
        print("展示注册界面")

        animation = QPropertyAnimation(register_pane)
        animation.setTargetObject(register_pane)
        animation.setPropertyName(b"pos")
        animation.setStartValue(QPoint(0, login_pane.height()))
        animation.setEndValue(QPoint(0, 0))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)


    def check_login(account, pwd):
        if account == "12345" and pwd == "itlike":
            print("登陆成功")

            caculator_pane.show()
            login_pane.hide()

        else:
            login_pane.show_error_animation()


    register_pane.exit_signal.connect(exit_register_pane)
    register_pane.register_account_pwd_signal.connect(lambda accout, pwd: print(accout, pwd))
    login_pane.show_register_pane_signal.connect(show_register_pane)
    login_pane.check_login_signal.connect(check_login)

    login_pane.show()

    sys.exit(app.exec_())
