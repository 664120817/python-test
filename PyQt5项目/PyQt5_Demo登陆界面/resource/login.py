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
        Form.resize(500, 450)
        Form.setMinimumSize(QtCore.QSize(500, 450))
        Form.setMaximumSize(QtCore.QSize(500, 450))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.login_top_bg_label = QtWidgets.QLabel(self.widget)
        self.login_top_bg_label.setStyleSheet("")
        self.login_top_bg_label.setText("")
        self.login_top_bg_label.setObjectName("login_top_bg_label")
        self.gridLayout.addWidget(self.login_top_bg_label, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.login_bottom = QtWidgets.QWidget(Form)
        self.login_bottom.setStyleSheet("")
        self.login_bottom.setObjectName("login_bottom")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.login_bottom)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 15)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.login_bottom)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.widget_3 = QtWidgets.QWidget(self.login_bottom)
        self.widget_3.setStyleSheet("")
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.auto_login_cb = QtWidgets.QCheckBox(self.widget_3)
        self.auto_login_cb.setObjectName("auto_login_cb")
        self.gridLayout_2.addWidget(self.auto_login_cb, 2, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.account_cb = QtWidgets.QComboBox(self.widget_3)
        self.account_cb.setMinimumSize(QtCore.QSize(0, 45))
        self.account_cb.setStyleSheet("QComboBox {\n"
"      font-size:20px;\n"
"      border:none;\n"
"      border-bottom:1px solid lightgray;\n"
"      background-color: transparent;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"        border-bottom:1px solid gray;\n"
"}\n"
"QComboBox:focus {\n"
"         border-bottom:1px solid rgb(18,183,245);\n"
"}\n"
"QComboBox::drop-down{\n"
"         background-color: transparent;\n"
"         width:60px;\n"
"         height:40px;\n"
"}\n"
"QComboBox::down-arrow{\n"
"    image:url(:/login/images/logni_combobox_icon.jpg);\n"
"    width:20px;\n"
"    height:15px;\n"
"}\n"
"QComboBox QAbstractItemView{\n"
"      min-height:60px;\n"
"}\n"
"QComboBox QAbstractItemView:item{\n"
"      color:lightblue;\n"
"}\n"
"    \n"
"")
        self.account_cb.setEditable(True)
        self.account_cb.setObjectName("account_cb")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/login/images/logni_item_icon2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.account_cb.addItem(icon, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/login/images/logni_item_icon1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.account_cb.addItem(icon1, "")
        self.gridLayout_2.addWidget(self.account_cb, 0, 0, 1, 2)
        self.pwd_le = QtWidgets.QLineEdit(self.widget_3)
        self.pwd_le.setMinimumSize(QtCore.QSize(0, 45))
        self.pwd_le.setStyleSheet("QLineEdit{\n"
"      font-size:20px;\n"
"      border:none;\n"
"      border-bottom:1px solid lightgray;\n"
"      background-color: transparent;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"        border-bottom:1px solid gray;\n"
"}\n"
"QLineEdit:focus {\n"
"         border-bottom:1px solid rgb(18,183,245);\n"
"}")
        self.pwd_le.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.pwd_le.setClearButtonEnabled(True)
        self.pwd_le.setObjectName("pwd_le")
        self.gridLayout_2.addWidget(self.pwd_le, 1, 0, 1, 2)
        self.remember_pwd_cb = QtWidgets.QCheckBox(self.widget_3)
        self.remember_pwd_cb.setObjectName("remember_pwd_cb")
        self.gridLayout_2.addWidget(self.remember_pwd_cb, 2, 1, 1, 1, QtCore.Qt.AlignRight)
        self.login_btn = QtWidgets.QPushButton(self.widget_3)
        self.login_btn.setEnabled(False)
        self.login_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.login_btn.setStyleSheet("QPushButton{\n"
"     \n"
"    background-color: rgb(33, 174,250);\n"
"    border-radius:5px;\n"
"    color:white;\n"
"    spacing:20px;\n"
"}\n"
"QPushButton:hover{\n"
"     background-color: rgb(72, 203,250);\n"
"}\n"
"QPushButton:pressed{\n"
"     background-color: rgb(85, 85,255);\n"
"}\n"
"QPushButton:disabled{\n"
"     background-color: rgb(117, 117, 117);\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/login/images/logni_btn_icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.login_btn.setIcon(icon2)
        self.login_btn.setIconSize(QtCore.QSize(25, 25))
        self.login_btn.setObjectName("login_btn")
        self.gridLayout_2.addWidget(self.login_btn, 4, 0, 1, 2)
        self.horizontalLayout.addWidget(self.widget_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.login_bottom)
        self.pushButton_2.setMinimumSize(QtCore.QSize(80, 80))
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 80))
        self.pushButton_2.setStyleSheet("border-image: url(:/login/images/QQ图片20190227192534.png);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 6)
        self.horizontalLayout.setStretch(2, 2)
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.widget_3.raise_()
        self.verticalLayout.addWidget(self.login_bottom)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 3)
        self.login_bottom.raise_()
        self.widget.raise_()
        self.widget.raise_()

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.show_register_pane)
        self.pushButton_2.clicked.connect(Form.open_qq_link)
        self.account_cb.editTextChanged['QString'].connect(Form.enable_login_btn)
        self.pwd_le.textChanged['QString'].connect(Form.enable_login_btn)
        self.auto_login_cb.clicked['bool'].connect(Form.auto_login)
        self.remember_pwd_cb.clicked['bool'].connect(Form.remember_pwd)
        self.login_btn.clicked.connect(Form.check_login)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "注册账号"))
        self.auto_login_cb.setText(_translate("Form", "自动登录"))
        self.account_cb.setItemText(0, _translate("Form", "12345"))
        self.account_cb.setItemText(1, _translate("Form", "23456"))
        self.remember_pwd_cb.setText(_translate("Form", "记住密码"))
        self.login_btn.setText(_translate("Form", "安全登录"))

import image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

