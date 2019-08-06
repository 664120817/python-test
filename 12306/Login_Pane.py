from PyQt5.Qt import *
from resource.login import Ui_Form
from API.API_TOOL import APITool

class DownLoadYZMThread(QThread):
    get_yzm_url_signal =pyqtSignal(str)
    def run(self):
        url = APITool.download_yzm()
        self.get_yzm_url_signal.emit(url)


class LoginPane(QWidget,Ui_Form):
    success_login =pyqtSignal(str)
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.setupUi(self)
        self.refresh_yzm()
        self.auto_enable_login_btn()
    def refresh_yzm(self):
        thread = DownLoadYZMThread(self)
        def parse_yzm_url(url):
            self.current_url = url
            print("刷新验证码")
            self.yzm_label.clear_points()
            # print(url)
            pixmap = QPixmap(url)
            self.yzm_label.setPixmap(pixmap)

        thread.get_yzm_url_signal.connect(parse_yzm_url)
        thread.start()


    def auto_dm(self):
        print("自动打码")

    def check_login(self):
        print("验证登录")
        result =self.yzm_label.get_result()
        if len(result) == 0:
            print("请填写验证码")
            return None
        if APITool.check_yzm(result):
            print("验证码正确")
            # 账号和密码
            account = self.account_le.text()
            pwd = self.pwd_le.text()
            #print(account,pwd)
            result_str=APITool.check_account_pwd(account,pwd)
            if result_str is None:
                QMessageBox.warning(self,"错误提示","账号或者密码错误")
                return None
            print(result_str)
            self.success_login.emit(result_str)

        else:
            print("验证码错误")
            self.yzm_label.clear_points()
            self.refresh_yzm()

    def auto_enable_login_btn(self):
        account =self.account_le.text()
        pwd =self.pwd_le.text()
        if len(account)==0 or len(pwd) ==0:
            self.login_btn.setEnabled(False)
        else:
            self.login_btn.setEnabled(True)

if __name__ ==  "__main__":
    import sys
    app = QApplication(sys.argv)
    long = LoginPane()
    long.show()
    sys.exit(app.exec_())