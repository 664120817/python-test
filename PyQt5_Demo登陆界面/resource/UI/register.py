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
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setStyleSheet("background-color:transparent;\n"
"color:rgb(241, 241, 241);\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setStyleSheet("font: 11pt \"楷体\";")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setStyleSheet("background-color:transparent;\n"
"color:rgb(241, 241, 241);\n"
"")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setStyleSheet("font: 11pt \"楷体\";")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_3.setStyleSheet("background-color:transparent;\n"
"color:rgb(241, 241, 241);\n"
"")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setStyleSheet("QPushButton{\n"
"     \n"
"    \n"
"    \n"
"    \n"
"    background-color: rgb(255, 255, 127);\n"
"    \n"
"    color: rgb(0, 0, 0);\n"
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
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        self.retranslateUi(Form)
        self.main_menue_btn.clicked.connect(Form.show_hide_menue)
        self.about_menue_btn.clicked.connect(Form.about_lk)
        self.reset_menue_btn.clicked.connect(Form.reset)
        self.exit_menue_btn.clicked.connect(Form.exit_pane)
        self.pushButton.clicked.connect(Form.check_register)
        self.main_menue_btn.clicked['bool'].connect(Form.show_hide_menue)
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
        self.pushButton.setText(_translate("Form", "注册"))

import image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

