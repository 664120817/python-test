from PyQt5.Qt import *
import requests
import os
import json
import re
import time
from urllib.parse import unquote,quote
class TimeTool(object):
    @staticmethod
    def getTrainFormatDate(train_date):
        date_arr=time.strptime(train_date,"%Y%m%d")
        time_tamp = time.mktime(date_arr)
        time_local =time.localtime(time_tamp)
        format = "%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)"
        return time.strftime(format, time_local)
        pass
class Config(object):
    seat_type_map_dic = {"1": "hard_seat", "9": "business_seat", "6": "vip_soft_bed", "4": "soft_bed", "3": "hard_bed",
               "O": "second_seat", "M": "first_seat", "F": "move_bed", "WZ": "no_seat",}
    @staticmethod
    def get_station_file_path():
        current_path = os.path.realpath(__file__)
        current_dir = os.path.split(current_path)[0]
        return current_dir +r"\stations.json"
    @staticmethod
    def get_yzm_file_path():
        current_path=os.path.realpath(__file__)
        current_dir= os.path.split(current_path)[0]
        print(current_dir)



class API(QObject):
    # 下载验证码GET
    GET_YZM_URL = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"
    # 验证码 Get
    #  login_site: E
    # module: login
    # rand: sjrand
    # 1552111693527:
    # callback: jQuery19108307760703551985_1552107987818
    # _: 1552107987833
    CHECK_YZM_URL = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    # 登陆验证  POST

    #username: 664120817 @ qq.com
    #password: 234556633
    #appid: otn
    CHECK_ACCOUNT_PWD_URL ="https://kyfw.12306.cn/passport/web/login"

    #问好 POST
    #appid:otn
    HELLOW_URL ="https://kyfw.12306.cn/otn/index/initMy12306Api"
    #uamtk
    UAMTK_URL ="https://kyfw.12306.cn/passport/web/auth/uamtk"
    #authorclient POST
    #tk:VmWwO58SmkarxfSa-_nY9K91l4xkTUmEc1Yl8P9WQy1iFYcnsd6160
    AUTHOR_URL ="https://kyfw.12306.cn/otn/uamauthclient"

    #验证用户是否登陆 POST
    # _json_att:
    IS_LOGIN_URL ="https://kyfw.12306.cn/otn/login/checkUser"

    #获取所有的城市GET
    STATIONS_URL ="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9090"
    #查询车票
    #leftTicketDTO.train_date: 2019 - 03 - 13
    #leftTicketDTO.from_station: BJP
    #leftTicketDTO.to_station: GZQ
    #purpose_codes: ADULT
    QUERY_TICKETS = "https://kyfw.12306.cn/otn/leftTicket/query?"

    #提交订单信息
    #secretStr: IGW7PrhFfkpAF7u7sZfNL7p7m3gvm9GljZ3Y7VurJKMWzC8AfeSb0tCm + 67
    #b3Lqqot40SM / jGL2W
    #F4trvtepbvPTlCpUI5AJyL9JHOg7vSbh4flQhqbCRTvsnyDC846LG5FI8T4smtgr2rwxYkmmdpRY
    #NI3qVRxbLP6fJEqHvxMq3C5xJ6X8wC / 1
    #ra / WU + Yro / x2trCmxfZmKPcQTKei9fkVQnfcFMQ6 / ZMr
    #7
    #ROlt78KKISaOuZzK / BgYwJA2 + JXxiRhs0CCsxnv + lSBLqYfZgwLCPa9WQWrg8wR / KPJNpG8wIPY
    # train_date: 2019 - 03 - 16
    # back_train_date: 2019 - 03 - 16
    # tour_flag: dc
    # purpose_codes: ADULT
    # query_from_station_name: 北京
    # query_to_station_name: 上海
    # undefined:
    SUBMIT_ORDER_REQUEST_URL="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"

    #initDc POST
    #_json_att:
    INIT_DC_URL ="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    #获取身份证信息POST
    # _json_att:
    # REPEAT_SUBMIT_TOKEN: deff1ac873fde386bfdd21ab74ad4b1e
    PassengerDTO_URL="https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"

    # 提交校验订单POST
    # cancel_flag: 2
    # bed_level_order_num: 000000000000000000000000000000
    # passengerTicketStr: O, 0, 1, 姓名, 1, 证件号码, 手机号码, N  席别（软卧等待），
    # oldPassengerStr: 姓名, 1, 证件号码, 1
    # _
    # tour_flag: dc
    # randCode:
    # whatsSelect: 1
    # _json_att:
    # REPEAT_SUBMIT_TOKEN: 87
    # a2e14d420af25be863e7062fa1fefe
    CHECK_ORDER_URL = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"

    # 获取队列个数 POST
    # train_date: Thu Feb 28 2019 00: 00:00 GMT + 0800(中国标准时间)
    # train_no: 61000G964501
    # stationTrainCode: G9645
    # seatType: O
    # fromStationTelecode: YQA
    # toStationTelecode: IZQ
    # leftTicket: S6m8spxaP0JWuXMzMXKdiIhm7PcdVT4%2BKLB81Cyg1Dif4etc
    # purpose_codes: 00
    # train_location: Q6
    # _json_att:
    # REPEAT_SUBMIT_TOKEN: 58726
    GET_QUEUECOUNT_TUL = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"

    # 确定订单  POST
    CONFIRMSINGLEFORQUEUE_URL = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
class APITool(QObject):
    session = requests.session()

    @classmethod
    def download_yzm(cls):
        response = cls.session.get(API.GET_YZM_URL)
        yzm_file_path =Config.get_yzm_file_path()
        # print(response.content)
        with open("yzm_file_path", "wb") as f:
            f.write(response.content)
        # print(cls.session.cookies)
        return "yzm_file_path"


    @classmethod
    def check_yzm(cls,yzm):
        print(yzm)
        data_dic = {
            #"callback": "jQuery191037043257607249735_1550240582305",
            "answer": yzm,
            "rand": "sjrand",
            "login_site": "E",
            #"_": "1550240582307"
        }
        response = cls.session.post(API.CHECK_YZM_URL,data=data_dic)
        print("校验结果",response.text)
        dic =response.json()
        return dic["result_code"] == "4"
        #print(type(response.json()))
        #result = response.findall(r'.*"(.*)"\}.*',response.text)[0]
        #return result == "4"
       # print(response.text)
       # print(response.json(["result_code"]))

    @classmethod
    def check_account_pwd(cls,account,pwd):
        data_dic = {
             "username": account,
             "password": pwd,
             "appid": "otn"
        }
        response = cls.session.post(API.CHECK_ACCOUNT_PWD_URL, data=data_dic)
        result_code = response.json()["result_code"]
        if result_code == 0:
            cls.author()
            return"".join( cls.get_hello())
        else:
            return None

        #print(cls.session.cookies)

    @classmethod
    def author(cls):
        resoponse = cls.session.post(API.UAMTK_URL,data={"appid":"otn"})
        tk = resoponse.json()["newapptk"]
        res2 =cls.session.post(API.AUTHOR_URL,data={"tk":tk})
        #cls.get_hello()
        #print(res2.text)
        #print(cls.session.cookies)

    @classmethod
    def get_hello(cls):
         response = cls.session.post(API.HELLOW_URL)
         dic=response.json()
         if dic["httpstatus"] == 200:
            return (dic["data"]["user_name"] , dic ["data"] ["user_regard"])
         return ("","")

    @staticmethod
    def get_all_stations_reverse():
        dic =APITool.get_all_stations()
        reverse_dic = {value:value for key,value in dic.items() }
        return reverse_dic

    @staticmethod
    def get_all_stations():
        #1检查本地是否有对应的缓存
        #2.有 直接加载 返回出去
        #3.没有 发送网络请求，请求结果保存到本地进行缓存
        if os.path.exists(Config.get_station_file_path()):
            with open(Config.get_station_file_path(),"r",encoding="utf-8") as f:
                result= json.loads(f.read(),encoding="utf-8")
                print(result)

            print("读取缓存")
        else:
            print("网络请求下载的站点数据")
        station_dic ={}
        resp =requests.get(API.STATIONS_URL)
        items=resp.text.split("@")
        for item in items:
            station_list = item.split("|")
            if len(station_list) !=6:
                continue
            #print(station_list)
            city_name = station_list[1]
            city_code= station_list[2]
            station_dic[city_name] =city_code
       # print(station_dic)
        with open(Config.get_station_file_path(),"w",encoding="utf-8") as f:
            json.dump(station_dic,f)
        return station_dic

    @staticmethod
    def get_all_statioms_reverse():
        print("API_Tool.get_all_statioms_reverse启动：准备反转城市站点字典")
        dic = APITool.get_all_stations()
        reverse_dic = {value:key for key,value in dic.items()}
        print("API_Tool.get_all_stations退出：返回反转城市站点字典")
        return  reverse_dic

    @classmethod
    def query_tickets(cls,train_date,from_station,to_station,purpose_codes,comboBox="",comboBox_2="",comboBox_3="",comboBox_4="",comboBox_5="",seat_type=None):

        cls.query_dic={

            "train_data": train_date,
            "purpose_codes": purpose_codes,
            "seat_type":seat_type,



        }
        code2station =APITool.get_all_statioms_reverse()
        query_params = {
            "leftTicketDTO.train_date": train_date,
            "leftTicketDTO.from_station": from_station,
            "leftTicketDTO.to_station": to_station,
            "purpose_codes": purpose_codes
        }
        print("query_tickets的传递字典",query_params)
        resp = requests.get(API.QUERY_TICKETS,params=query_params)
        result = resp.json()
        print("query_tickets返回的json数据进行处理")
        trainDicts =[]
        if result["httpstatus"] == 200:
            items = result["data"]["result"]
            #print(items)
            for item in items:
                trainDict = {}
                trainInfo = item.split('|')
                if trainInfo[11] == "Y": #是否可以预定
                    trainDict["secret_str"] = trainInfo[0] #车次密文字符串（下订单使用）
                    trainDict["train_num"] = trainInfo[2] #车次编号 6c000G962802
                    trainDict["train_name"] = trainInfo[3]  # 车次名称  如G9628
                    trainDict["from_station_code"] = trainInfo[4] #出发电报码
                    trainDict["to_station_code"] = trainInfo[5] #目的地电报码
                    trainDict["from_station_name"] = code2station[trainInfo[6]] #出发地名称
                    trainDict["to_station_name"] = code2station[trainInfo[7]] #目的地名称
                    trainDict["start_time"] = trainInfo[8]
                    trainDict["arrive_time"] = trainInfo[9]
                    trainDict["total_time"] = trainInfo[10] #出发-到达-总时间
                    trainDict["left_ticket"] = trainInfo[12] #余票
                    trainDict["train_data"] = trainInfo[13] #火车日期
                    trainDict["train_location"] = trainInfo[15] #P4 后期用
                    trainDict["vip_soft_bed"] = trainInfo[21] #高级软卧
                    trainDict["other_seat"] = trainInfo[22] #其他
                    trainDict["soft_bed"] = trainInfo[23] #软卧
                    trainDict["no_seat"] = trainInfo[26] #无座
                    trainDict["hard_bed"] = trainInfo[28] #硬卧
                    trainDict["hard_seat"] = trainInfo[29] #硬座
                    trainDict["second_seat"] = trainInfo[30] #二等
                    trainDict["first_seat"] = trainInfo[31] #一等座
                    trainDict["business_seat"] = trainInfo[32] #商务座
                    trainDict["move_bed"] = trainInfo[33] #动卧
                    if seat_type == None :

                         trainDicts.append(trainDict)
                         print("查询余票")
                    else:
                        key = Config.seat_type_map_dic[seat_type]
                        if trainDict[key] == "有" or trainDict[key].isdigit():
                          if trainDict["train_name"] == comboBox or trainDict["train_name"]==comboBox_2 or trainDict["train_name"]==comboBox_3 or trainDict["train_name"]==comboBox_4 or trainDict["train_name"]==comboBox_5:
                             trainDicts.append(trainDict)
                             print("有票")

        else:
            print("数据请求错误")

        return trainDicts

       # print("query_tickets已经查询结果：",response.json())
       # result = response.json()
        print("query_tickets返回的json数据进行处理")

    @classmethod
    def check_login(cls):
        rep=cls.session.post(API.IS_LOGIN_URL,data={"_json_att":""})
        is_login=rep.json()["data"]["flag"]
        return is_login

    @classmethod
    def submit_order_request(cls,trainDict):
        data_dic = {
            "secretStr": unquote(trainDict["secret_str"]),
            "train_date": trainDict["train_data"],
            "back_train_date": trainDict["train_data"],
            "tour_flag": "dc",
            "purpose_codes": cls.query_dic["purpose_codes"],
            "query_from_station_name": trainDict["from_station_name"],
            "query_to_station_name": trainDict["to_station_name"],
            "undefined": ""

        }
        print(data_dic)
        rep = cls.session.post(API.SUBMIT_ORDER_REQUEST_URL, data=data_dic)
        status = rep.json()["status"]
        if not status:
            print(rep.json()["messages"])
            return False
        print("继续订票")
        return True

    @classmethod
    def initDC(cls):
        rep=cls.session.post(API.INIT_DC_URL,data={"_json_att":""})
        try:
            token = re.findall(r"var globalRepeatSubmitToken = '(.*?)'",rep.text)[0]
            key_check_isChange = re.findall(r"'key_check_isChange':'(.*?)'", rep.text)[0]
            return (token,key_check_isChange)

        except:
            return None
        print("-"*30)
        print(token)

    @classmethod
    def get_PassengerDTO(cls,token,name=""):
        data_dic ={
            "_json_att":"",
            "REPEAT_SUBMIT_TOKEN": token
        }
        rep=cls.session.post(API.PassengerDTO_URL,)
        result=rep.json()
        if not result["status"]:
            print("获取乘客信息失败")
            return None
        name = cls.get_hello()[0]
        print("乘客信息",name)
        for dic in result["data"]["normal_passengers"]:
            if dic["passenger_name"]==name:
                return dic
        return None

    @classmethod
    def checkOrder(cls,seatType,passengerDic,token):
        data_dic ={
            "cancel_flag":"2",
            "bed_level_order_num":"000000000000000000000000000000",
            "passengerTicketStr":"{},{},{},{},{},{},{},N".format(seatType,passengerDic["passenger_flag"],
passengerDic["passenger_type"],
passengerDic["passenger_name"],
passengerDic["passenger_id_type_code"],
passengerDic["passenger_id_no"],
passengerDic["mobile_no"]),
            "oldPassengerStr":"{},{},{},1_".format(passengerDic["passenger_name"],passengerDic["passenger_id_type_code"],passengerDic["passenger_id_no"]),
            "tour_flag":"dc",
            "randCode":"",
            "whatsSelect": "1",
            "_json_att":"",
            "REPEAT_SUBMIT_TOKEN":token
        }
        print(data_dic)
        rep=cls.session.post(API.CHECK_ORDER_URL,data=data_dic)
        result=rep.json()
        if result["status"] and result["data"]["submitStatus"]:
            print("检查订单成功")
            return True
        return False

    @classmethod
    def getQueuCount(cls,trainDic,seatType,token):
        data_dic ={

            # 20190220
            # Thu Feb 28 2019 00: 00:00 GMT + 0800(中国标准时间)
            "train_date": TimeTool.getTrainFormatDate(trainDic["train_data"]),
            "train_no": trainDic["train_num"],  # 61000G964501
            "stationTrainCode": trainDic["train_name"],
            "seatType": seatType,  # 座席
            "fromStationTelecode": trainDic["from_station_code"],  # YQA
            "toStationTelecode": trainDic["to_station_code"],  # IZQ
            "leftTicket": trainDic["left_ticket"],
            "purpose_codes": "00",
            "train_location": trainDic["train_location"],
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": token

        }
        rep=cls.session.post(API.GET_QUEUECOUNT_TUL,data=data_dic)
        result = rep.json()
        if not result["status"]:
            print("查询队列消息失败")
            return False
        print("查询队列个数成功",result["data"]["ticket"])
        return True

    @classmethod
    def confirm_queue(cls,seatType,token,key_check_isChange,passengerDic,trainDic):
        data_dic ={

            "passengerTicketStr": "{},{},{},{},{},{},{},N".format(seatType, passengerDic["passenger_flag"],
                                                                  passengerDic["passenger_type"],
                                                                  passengerDic["passenger_name"],
                                                                  passengerDic["passenger_id_type_code"],
                                                                  passengerDic["passenger_id_no"],
                                                                  passengerDic["mobile_no"]),
            "oldPassengerStr": "{},{},{},1_".format(passengerDic["passenger_name"],
                                                    passengerDic["passenger_id_type_code"],
                                                    passengerDic["passenger_id_no"]),
            "randCode": "",
            "purpose_codes": "00",
            "key_check_isChange": key_check_isChange,
            "leftTicketStr": trainDic["left_ticket"],
            "train_location": trainDic["train_location"],
            "choose_seats": "",#选择座位
            "seatDetailType": "000",
            "whatsSelect": "1",
            "roomType": "00",
            "daALL": "N",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": token

        }
        rep=cls.session.post(API.CONFIRMSINGLEFORQUEUE_URL,data=data_dic)
        result =rep.json()
        return result["status"] and result["data"]["submitStatus"]


    @classmethod
    def buy_ticket(cls,trainDict=None,name=""):
        if not cls.check_login():
            print("请先登陆账户")
            return False
        #print(trainDict)
        if not cls.submit_order_request(trainDict):
            print("提交订单请求失败")
            return False
        token,key_check_isChange= cls.initDC()
        passenger=cls.get_PassengerDTO(token,name)

        print(passenger)
        if not cls.checkOrder(cls.query_dic["seat_type"],passenger,token):
               print("检查订单失败")
               return False

        if not cls.getQueuCount(trainDict,cls.query_dic["seat_type"],token):
            print("查询队列个数失败")
            return False
        if not cls.confirm_queue(cls.query_dic["seat_type"],token,key_check_isChange,passenger,trainDict,):
            print("预定失败")
            return False
        return True








if __name__ == '__main__':
    APITool.buy_ticket()

