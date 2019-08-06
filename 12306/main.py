from PyQt5.Qt import *

from Login_Pane import LoginPane
from Query_Pane import QueryPane


if __name__ == '__main__':
        import sys
        app = QApplication(sys.argv)

        login_pane = LoginPane()
        query_pane = QueryPane()

        def success_login_slot(content):
            login_pane.hide()#隐藏窗口

            query_pane.setWindowTitle(content)
            query_pane.show()
        login_pane.success_login.connect(success_login_slot)
        login_pane.show()

        sys.exit(app.exec_())
