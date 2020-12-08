from PyQt5.Qt import *
from  resource.query_pane import Ui_Form
from API.API_TOOL import APITool
from Book_Pane import BookPane
class QueryPane(QWidget,Ui_Form):
    def __init__(self,parent=None,*args,**kwargs):
         super().__init__(parent,*args,**kwargs)
         self.tj ={'zw': None, 'phone_num': None}
         self.setupUi(self)
         self.setupBookPane()
         self.setupData()
    def resizeEvent(self, evt):
        super().resizeEvent(evt)
        self.book_pane.resize(self.width(),self.query_pane_top.height())

    def hide_book_pane(self):
        animation = QPropertyAnimation(self.book_pane, b"pos", self.book_pane)
        animation.setEndValue(QPoint(0, -self.book_pane.height()))
        animation.setStartValue(QPoint(0, 0))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    def show_book_pane(self):
        animation = QPropertyAnimation(self.book_pane, b"pos", self.book_pane)
        animation.setStartValue(QPoint(0, -self.book_pane.height()))
        animation.setEndValue(QPoint(0, 0))
        animation.setDuration(1000)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

    def setupBookPane(self):
        self.book_pane = BookPane(self)
        self.book_pane.confirm_signal.connect(self.book_ticket_filter)
        self.book_pane.cancel_signal.connect(self.cancel_query)
        self.book_pane.resize(self.width(), 150)
        self.book_pane.move(0, -self.book_pane.height())
        self.book_pane.show()


    def setupData(self):
        dic = APITool.get_all_stations()
        self.from_station_cb.addItems(dic.keys())
        self.to_station_cb.addItems(dic.keys())
        completer =QCompleter(dic.keys())
        self.from_station_cb.setCompleter(completer)
        def check_data(cb):
            current_city = cb.currentText()
            result = dic.keys().__contains__(current_city)
            if not result:
                  # cb.clearEditText()
                    cb.setCurrentIndex(0)
            pass
        self.from_station_cb.lineEdit().editingFinished.connect(lambda :check_data(self.from_station_cb))
        completer2 = QCompleter(dic.keys())
        self.to_station_cb.setCompleter(completer2)
        self.to_station_cb.lineEdit().editingFinished.connect(lambda: check_data(self.to_station_cb))
        self.start_date_de.setDate(QDate.currentDate())
        self.start_date_de.setMinimumDate(QDate.currentDate())



        #设置表格的头部数据
        model =QStandardItemModel(self.tickets_tv)
        #设置模型的头部数据
        headers=["车次","出发站-到达站","出发时间-到达时间","历时","商务座-特等座","一等座","二等座","高级-软卧","软卧-一等卧","动卧","硬卧-二等卧","硬座","无座","其他",]

        model.setColumnCount(len(headers))
        for idx,title in enumerate(headers):
            model.setHeaderData(idx,Qt.Horizontal,title)

        self.tickets_tv.setModel(model)
    def filter_tickets(self):
        print("开始查询")

        dic = APITool.get_all_stations()  # 出发时间
        start_data = self.start_date_de.text()  # 类型
        from_city_code = dic[self.from_station_cb.currentText()]  # 目的地
        to_city_code = dic[self.to_station_cb.currentText()]# 出发地
        purpose_codes = self.buttonGroup.checkedButton().property("q_value")
        print("filter_tickets筛选需要数据：", self.tj)
        print(self.to_station_cb.currentText())
        comboBox = self.comboBox.currentText()
        comboBox_2 = self.comboBox_2.currentText()
        comboBox_3 = self.comboBox_3.currentText()
        comboBox_4 = self.comboBox_4.currentText()
        comboBox_5 = self.comboBox_5.currentText()
        print(comboBox, comboBox_2, comboBox_3, comboBox_4, comboBox_5)
        result = APITool.query_tickets(start_data, from_city_code, to_city_code, purpose_codes,comboBox,comboBox_2,comboBox_3,comboBox_4,comboBox_5,seat_type=self.tj["zw"])
        print("filter_tickets函数成功获取到数据")
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()

        return result
    def query_tickets(self):
        result =self.filter_tickets()
        for i in result:
            dic = [(i["train_name"])]
            print(dic)
            self.comboBox.addItems(dic)
            self.comboBox_2.addItems(dic)
            self.comboBox_3.addItems(dic)
            self.comboBox_4.addItems(dic)
            self.comboBox_5.addItems(dic)
            print("抢票")
        print(result)
        model = self.tickets_tv.model()
        #QStandardItemModel().setItem(0,0,QStandardItem("N97"))
        model.setRowCount(len(result))

        columns =["train_name",("from_station_name", "to_station_name"),("start_time", "arrive_time"),"total_time",
         "business_seat","first_seat","second_seat","vip_soft_bed","soft_bed","move_bed","hard_bed","hard_seat","no_seat","other_seat"]
        for row,train_dic in enumerate(result):
            print(train_dic)
            for column,column_name in enumerate(columns):
                if train_dic:
                   if type(column_name) == str:
                       model.setItem(row,column,QStandardItem(train_dic[column_name]))

                   else:
                       tmp ="->".join([train_dic[key] for key in column_name])
                       model.setItem(row, column, QStandardItem(tmp))

                else:
                    model.setItem(row, 0, QStandardItem("列出停运或者没票"))
        self.tickets_tv.setModel(model)


        return result
        print("query_tickets:函数成返回")

    def book_ticket_filter(self,tj):
        #self.hide_book_pane()
        #{'zw':'F','phone_num':'123'}
        print("TJ",tj)
        self.tj = tj
        self.timer.start(3000)


    def book_tickets(self):
        print("抢票")
        self.show_book_pane()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.buy_ticket)

    def buy_ticket(self):
        "不断查询"
        result = self.query_tickets()
        if len(result):
            self.cancel_query()
            print("当前有车票,正在下单")
            success=APITool.buy_ticket(result[0])  # (result[0])
            if success:
                print("下单成功,请立即支付")
                QMessageBox.information(self, "恭喜", "订票成功，请立即去支付!")
            else:
                print("下单失败!!!")
                QMessageBox.warning(self, "错误提示", "订票失败!")
        else:
            print("没有查询到车票")

    def cancel_query(self):
        print("取消")
        self.timer.stop()
        self.hide_book_pane()
        self.tj = {'zw': None, 'phone_num': None}



if __name__ == '__main__':
        import sys
        app = QApplication(sys.argv)

        querypane= QueryPane()
        querypane.show()

        sys.exit(app.exec_())
