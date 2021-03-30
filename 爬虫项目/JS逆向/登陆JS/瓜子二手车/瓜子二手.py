# 导入需要的模块
import requests
import parsel
import execjs
import csv


class GuaZiCarSpider:
    """爬取瓜子二手车信息"""

    def __init__(self, page):
        self.GZ_URL = 'https://www.guazi.com/www/buy/o{}c-1/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 FS"
        }
        self.CAR_INFOS = ['汽车品牌', '汽车信息', '现价', '原价']
        self.PAGE = page

    def get_js_data(self, url):
        """
        发送请求，获取响应数据,并提取js需要用的数据的方法
        :param url:
        :return:
        """
        response = requests.get(url, headers=self.headers)
        html = parsel.Selector(response.content.decode('utf-8'))
        # 提取需要js需要的两个参数
        cookie_data = html.re("anti\('(.*?)','(\d+)'\);")
        return cookie_data

    def get_js_cookie(self, cookie_data):
        """
        逆向瓜子的js的方法
        :param cookie_data:
        :return:
        """
        with open('./guazi.js', 'r', encoding='utf-8') as jsfile:
            js_code = jsfile.read()
            d_js = execjs.compile(js_code)
            cookie = d_js.eval(f'get_cookie("{cookie_data[0]}","{cookie_data[1]}")')
            return cookie

    def get_headers(self, cookie):
        """
        构建新的headers的方法
        :param cookie:
        :return:
        """
        headers = {
            'Cookie': cookie,
            "Host": "www.guazi.com",
            "Referer": f"https://www.guazi.com/www/buy/o{str(self.PAGE)}c-1/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 FS"
        }
        return headers

    def parse_url2(self, url, headers):
        """
        发送请求，获取响应的数据的方法
        :param url:
        :param headers:
        :return:
        """
        response = requests.get(url, headers=headers)
        return response.content.decode('utf-8')

    def get_car_data(self, html_str):
        """
        提取二手车数据信息的方法
        :param html_str:
        :return:
        """
        html = parsel.Selector(html_str)
        # 提取汽车品牌列表
        car_title_list = html.css('.carlist.clearfix.js-top>li>a::attr(title)').extract()
        # 提取汽车信息列表
        car_infos = html.css('.carlist.clearfix.js-top>li>a>.t-i::text').extract()
        car_info_list = ["|".join(car_infos[i:i + 3]) for i in range(0, len(car_infos), 3)]
        # 提取汽车现价
        current_prices = html.css('.carlist.clearfix.js-top>li>a>.t-price>p::text').extract()
        current_price_list = [current_prices[i] + '万' for i in range(0, len(current_prices), 2)]
        # 提取汽车原价
        original_price_list = html.css('.carlist.clearfix.js-top>li>a>.t-price>.line-through::text').extract()
        return car_title_list, car_info_list, current_price_list, original_price_list

    def run(self):
        """
        实现主要逻辑思路
        :return:
        """
        with open("./guazi.csv", 'a', encoding='utf-8-sig', newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.CAR_INFOS)
            # 1.提取js逆向需要的数据
            cookie_data = self.get_js_data(self.GZ_URL.format(str(self.PAGE)))
            # 2.js逆向，得到需要的cookie
            cookie = self.get_js_cookie(cookie_data)
            # 3.构建新的请求头
            headers = self.get_headers(cookie)
            # 4.发送请求，获取响应的数据
            html_str = self.parse_url2(self.GZ_URL.format(str(self.PAGE)), headers)
            # 5.提取二手车的信息列表
            car_title_list, car_info_list, current_price_list, original_price_list = self.get_car_data(html_str)
            for car_title, car_info, current_price, original_price in zip(car_title_list, car_info_list,
                                                                          current_price_list,
                                                                          original_price_list):
                car_data = [car_title, car_info, current_price, original_price]
                print(car_data)
                # 6.保存数据
                writer.writerow(car_data)


if __name__ == '__main__':
    for page in range(1, 7):
        guazicar_spider = GuaZiCarSpider(page)
        guazicar_spider.run()
