from PyQt5.Qt import *

class CaculatorBtn(QPushButton):

    key_pressed=pyqtSignal(str,str)
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
       # self.setAutoExclusive(True)
    def mousePressEvent(self, *args, **kwargs):
        super().mousePressEvent(*args, **kwargs)
        self.key_pressed.emit(self.text(),self.property("role"))



    def resizeEvent(self, *args, **kwargs):
        super().resizeEvent(*args, **kwargs)
        self.setStyleSheet("""
        QPushButton[bg='gray']  {
             color:white;
             background-color:rgb(88,88,88);
        }     
        QPushButton[bg='gray']:hover  {
             background-color:rgb(150,150,150);
        }    
        QPushButton[bg='orange'], QPushButton[bg='equal'] {
             color:white;
             background-color:rgb(207,138,0);
        }      
        QPushButton[bg='orange']:hover,QPushButton[bg='equal']:hover {
             background-color:rgb(238,159,0);
        }
        QPushButton[bg='orange']:checked {
             background-color:white;
             color:rgb(207,138,0)
        }

        QPushButton[bg='lightgray']  {
             color:black;
             background-color:rgb(200,200,200);
        }    
        QPushButton[bg='lightgray']:hover {
             background-color:rgb(230,230,230);
        }      
        QPushButton[bg] {
              font-size:20px;
              border-radius:%dpx;
        } 
                """ % (min(self.width(),self.height()) / 2))