from PyQt5.Qt import *
from resource.book_pane import Ui_Form

class BookPane(QWidget,Ui_Form):
    confirm_signal = pyqtSignal(dict)
    cancel_signal = pyqtSignal()
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)


    def confirm(self):

        zw=self.buttonGroup.checkedButton().property("val")
        phone_num =self.phone_num_le.text()
        print(zw,phone_num)


        self.confirm_signal.emit({"zw":zw,"phone_num":phone_num})#传递出数据

    def cancel_query(self):
        self.cancel_signal.emit()



if __name__ == '__main__':
        import sys
        app = QApplication(sys.argv)

        window = BookPane()
        window.show()

        sys.exit(app.exec_())
