# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 500)
        Form.setMinimumSize(QtCore.QSize(600, 500))
        Form.setMaximumSize(QtCore.QSize(600, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMinimumSize(QtCore.QSize(450, 400))
        self.widget.setMaximumSize(QtCore.QSize(450, 400))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.yzm_label = SZLbel(self.widget)
        self.yzm_label.setMinimumSize(QtCore.QSize(293, 188))
        self.yzm_label.setMaximumSize(QtCore.QSize(293, 190))
        self.yzm_label.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.yzm_label.setObjectName("yzm_label")
        self.gridLayout.addWidget(self.yzm_label, 2, 1, 3, 1)
        self.login_btn = QtWidgets.QPushButton(self.widget)
        self.login_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.login_btn.setObjectName("login_btn")
        self.gridLayout.addWidget(self.login_btn, 5, 0, 1, 2)
        self.pwd_le = QtWidgets.QLineEdit(self.widget)
        self.pwd_le.setMinimumSize(QtCore.QSize(0, 45))
        self.pwd_le.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd_le.setClearButtonEnabled(True)
        self.pwd_le.setObjectName("pwd_le")
        self.gridLayout.addWidget(self.pwd_le, 1, 0, 1, 2)
        self.account_le = QtWidgets.QLineEdit(self.widget)
        self.account_le.setMinimumSize(QtCore.QSize(0, 45))
        self.account_le.setClearButtonEnabled(False)
        self.account_le.setObjectName("account_le")
        self.gridLayout.addWidget(self.account_le, 0, 0, 1, 2)
        self.pwe_le = QtWidgets.QPushButton(self.widget)
        self.pwe_le.setMinimumSize(QtCore.QSize(50, 50))
        self.pwe_le.setMaximumSize(QtCore.QSize(50, 50))
        self.pwe_le.setObjectName("pwe_le")
        self.gridLayout.addWidget(self.pwe_le, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_2.setMaximumSize(QtCore.QSize(50, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        self.pwe_le.clicked.connect(Form.refresh_yzm)
        self.pushButton_2.clicked.connect(Form.auto_dm)
        self.login_btn.clicked.connect(Form.check_login)
        self.account_le.textChanged['QString'].connect(Form.auto_enable_login_btn)
        self.pwd_le.textChanged['QString'].connect(Form.auto_enable_login_btn)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.yzm_label.setText(_translate("Form", "TextLabel"))
        self.login_btn.setText(_translate("Form", "登陆"))
        self.pwd_le.setPlaceholderText(_translate("Form", "请输入真实的12306密码"))
        self.account_le.setText(_translate("Form", "664120817@qq.com"))
        self.account_le.setPlaceholderText(_translate("Form", "请输入真正的12306账号"))
        self.pwe_le.setText(_translate("Form", "刷新"))
        self.pushButton_2.setText(_translate("Form", "打码"))

from Sz_Label import SZLbel

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

