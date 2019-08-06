# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 450)
        Form.setMinimumSize(QtCore.QSize(500, 450))
        Form.setMaximumSize(QtCore.QSize(500, 450))
        Form.setStyleSheet("QWidget#Form{\n"
"   border-image: url(:/reqister/images/register_background.jpg.jpg);\n"
"   }")
        self.main_menue_btn = QtWidgets.QPushButton(Form)
        self.main_menue_btn.setGeometry(QtCore.QRect(10, 20, 51, 51))
        self.main_menue_btn.setStyleSheet("QPushButton{\n"
"    border-radius:25px;\n"
"       \n"
"    background-color: rgb(255, 170, 255);\n"
"    border:2px solid rgb(250,218,218);\n"
"    color:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    \n"
"    border:8px double rgb(239,160,179);\n"
"    \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"   \n"
"   \n"
"    background-color: rgb(255, 0, 127);\n"
"    \n"
"}")
        self.main_menue_btn.setCheckable(True)
        self.main_menue_btn.setObjectName("main_menue_btn")
        self.about_menue_btn = QtWidgets.QPushButton(Form)
        self.about_menue_btn.setGeometry(QtCore.QRect(80, 20, 51, 51))
        self.about_menue_btn.setStyleSheet("QPushButton{\n"
"    border-radius:25px;\n"
"       \n"
"    background-color: rgb(255, 170, 255);\n"
"    border:2px solid rgb(250,218,218);\n"
"    color:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    \n"
"    border:8px double rgb(239,160,179);\n"
"    \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"   \n"
"   \n"
"    background-color: rgb(255, 0, 127);\n"
"    \n"
"}")
        self.about_menue_btn.setCheckable(False)
        self.about_menue_btn.setObjectName("about_menue_btn")
        self.exit_menue_btn = QtWidgets.QPushButton(Form)
        self.exit_menue_btn.setGeometry(QtCore.QRect(10, 90, 51, 51))
        self.exit_menue_btn.setStyleSheet("QPushButton{\n"
"    border-radius:25px;\n"
"       \n"
"    background-color: rgb(255, 170, 255);\n"
"    border:2px solid rgb(250,218,218);\n"
"    color:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    \n"
"    border:8px double rgb(239,160,179);\n"
"    \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"   \n"
"   \n"
"    background-color: rgb(255, 0, 127);\n"
"    \n"
"}")
        self.exit_menue_btn.setCheckable(False)
        self.exit_menue_btn.setObjectName("exit_menue_btn")
        self.reset_menue_btn = QtWidgets.QPushButton(Form)
        self.reset_menue_btn.setGeometry(QtCore.QRect(90, 80, 51, 51))
        self.reset_menue_btn.setStyleSheet("QPushButton{\n"
"    border-radius:25px;\n"
"       \n"
"    background-color: rgb(255, 170, 255);\n"
"    border:2px solid rgb(250,218,218);\n"
"    color:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    \n"
"    border:8px double rgb(239,160,179);\n"
"    \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"   \n"
"   \n"
"    background-color: rgb(255, 0, 127);\n"
"    \n"
"}")
        self.reset_menue_btn.setCheckable(False)
        self.reset_menue_btn.setObjectName("reset_menue_btn")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(164, 219, 271, 153))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setStyleSheet("font: 11pt \"楷体\";")
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.account_le = QtWidgets.QLineEdit(self.layoutWidget)
        self.account_le.setMinimumSize(QtCore.QSize(0, 30))
        self.account_le.setStyleSheet("background-color:transparent;\n"
"color:rgb(241, 241, 241);\n"
"")
        self.account_le.setClearButtonEnabled(True)
        self.account_le.setObjectName("account_le")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.account_le)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setStyleSheet("font: 11pt \"楷体\";")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.password_le = QtWidgets.QLineEdit(self.layoutWidget)
        self.password_le.setMinimumSize(QtCore.QSize(0, 30))
        self.password_le.setStyleSheet("background-color:transparent;\n"
"color:rgb(241, 241, 241);\n"
"")
        self.password_le.setClearButtonEnabled(True)
        self.password_le.setObjectName("password_le")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password_le)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setStyleSheet("font: 11pt \"楷体\";")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.confirm_pwd_le = QtWidgets.QLineEdit(self.layoutWidget)
        self.confirm_pwd_le.setMinimumSize(QtCore.QSize(0, 30))
        self.confirm_pwd_le.setStyleSheet("background-color:transparent;\n"
"color:rgb(241, 241, 241);\n"
"")
        self.confirm_pwd_le.setClearButtonEnabled(True)
        self.confirm_pwd_le.setObjectName("confirm_pwd_le")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.confirm_pwd_le)
        self.register_btn = QtWidgets.QPushButton(self.layoutWidget)
        self.register_btn.setEnabled(False)
        self.register_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.register_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.register_btn.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: rgb(255, 255, 127);\n"
"    \n"
"    color: rgb(0, 0, 0);\n"
"    \n"
"}\n"
"\n"
"QPushButton:disabled{\n"
"    \n"
"    background-color: rgb(131, 131, 131);\n"
"    \n"
"    \n"
"    \n"
"}\n"
"QPushButton:hover{\n"
"       \n"
"    background-color: rgb(50, 255, 19);\n"
"}\n"
"QPushButton:pressed{\n"
"    \n"
"    background-color: rgb(255, 0, 0);\n"
"}\n"
"")
        self.register_btn.setObjectName("register_btn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.register_btn)
        self.about_menue_btn.raise_()
        self.exit_menue_btn.raise_()
        self.reset_menue_btn.raise_()
        self.layoutWidget.raise_()
        self.main_menue_btn.raise_()

        self.retranslateUi(Form)
        self.about_menue_btn.clicked.connect(Form.about_lk)
        self.reset_menue_btn.clicked.connect(Form.reset)
        self.exit_menue_btn.clicked.connect(Form.exit_pane)
        self.register_btn.clicked.connect(Form.check_register)
        self.main_menue_btn.clicked['bool'].connect(Form.show_hide_menue)
        self.account_le.textChanged['QString'].connect(Form.enable_register_btn)
        self.password_le.textChanged['QString'].connect(Form.enable_register_btn)
        self.confirm_pwd_le.textChanged['QString'].connect(Form.enable_register_btn)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.main_menue_btn.setText(_translate("Form", "菜单"))
        self.about_menue_btn.setText(_translate("Form", "关于"))
        self.exit_menue_btn.setText(_translate("Form", "退出"))
        self.reset_menue_btn.setText(_translate("Form", "重置"))
        self.label.setText(_translate("Form", "账    号："))
        self.label_2.setText(_translate("Form", "密    码："))
        self.label_3.setText(_translate("Form", "确认密码："))
        self.register_btn.setText(_translate("Form", "注册"))

import image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

