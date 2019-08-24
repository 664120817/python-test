"""
1，重写start_requests方法，根据分类信息构建表页的请求
2，解析列表页，提取商品的skuid，构建商品基本的信息请求；实现翻页
3，解析商品基本信息，构建商品促销信息的请求
4，解析促销信息，构建商品评价信息的请求
5，解析评价信息，构建商品价格信息的请求
6，解析价格信息
"""
import scrapy,json,pickle
from scrapy import Spider
from ..items import Product
from jsonpath import jsonpath
from scrapy_redis.spiders import RedisSpider
"""
分布式爬虫
1，修改爬虫类
修改继承关系：继承RedisSpider
指定redis_key
把重写start_requests 改为 make_request_from_data
"""
# 修改继承关系：继承RedisSpider
class JdProductSpider(RedisSpider):
    name = 'jd_product'
    allowed_domains = ['jd.com','dc.3.cn','p.3.cn']
    #用于指定起始URL列表，在Redis数据库中的key
    redis_key='jd_product:category'
    # 把重写start_requests    改为  make_request_from_data
    def make_request_from_data(self,data):
        """
        根据redis中读取的分类信息的二进制数据，构建请求
        :param data:分类信息的二进制数据
        :return:根据小分类URL，构建的请求对象
        """
        #把分类信息的二进制数据 转化为字典
        category=pickle.loads(data)
        #根据小分类的url，构建列表页的请求
        #注意：要使用return来返回一个请求，不要使用yield
        return scrapy.Request(category['s_category_url'],callback=self.parse,meta={'category':category})
    # def start_requests(self):
    #     # 重写start_requests方法，根据分类信息构建表页的请求
    #     category={'b_category_name': '家用电器',
    #      'b_category_url': 'https://jiadian.jd.com',
    #      'm_category_name': '电视',
    #      'm_category_url': 'https://list.jd.com/list.html?cat=737,794,798',
    #      's_category_name': '超薄电视',
    #      's_category_url': 'https://list.jd.com/list.html?cat=737,794,798&ev=4155_76344&sort=sort_rank_asc&trans=1&JL=2_1_0#J_crumbsBar'
    #               }
    #     #根据小分类URL构建请求
    #     yield scrapy.Request(url=category['s_category_url'],callback=self.parse,meta={'category':category['s_category_name']})
    def parse(self, response):
        category=response.meta['category']
        print(category)
        #解析列表页，提取商品的skuid
        sku_ids=response.xpath('//div[contains(@class,j-sku-item)]/@data-sku').getall()

        for sku_id in sku_ids: #创建Product,用于保存商品数据
            #设置商品类别
            item = Product()
            item['product_category']=category
            item['product_sku_id']=sku_id
            #构建基本商品信息请求
            product_base_url='https://cdnware.m.jd.com/c1/skuDetail/apple/7.0.0/{}.json'.format(sku_id)
            yield scrapy.Request(product_base_url,callback=self.product_base_base,meta={'item':item})
        #获取下一页的URL
        next_url=response.xpath("//a[@class='pn-next']/@href").get()
        if next_url: #补全url
            next_url=response.urljoin(next_url)
            print(next_url,"url")
        # 构建下一页url
        yield scrapy.Request(next_url,callback=self.parse,meta={'category':category})


    def product_base_base(self,response):
       item=response.meta['item']
       item=Product()
       response_json=json.loads(response.text)
       item['product_category'] =response.meta['item']['product_category']  # 商品类别
       item['product_sku_id']= response.meta['item']['product_sku_id']  # 商品ID
       item['product_name']= response_json['wareInfo']['basicInfo']['name']  # 商品名称
       item['product_img_url']=  response_json['wareInfo']['basicInfo']['wareImage'] [0]['big'] # 商品图片URL
       item['product_book_info']= response_json['wareInfo']['basicInfo']['bookInfo']  # 图书信息，作者，出版社
       #商品选项 注意colorSize:值是列表，而jsonpath返回列表，color_size是两层列表
       color_size=jsonpath(response_json,'$..colorSize')
       # color_size =response_json['wareInfo']['basicInfo']['colorSizeInfo']['colorSize']
       if color_size:
           color_size=color_size[0]
           product_option={}
           for option in color_size:
               title=option['title']
               value=jsonpath(option,'$..text')
               product_option[title]=value
           item['product_option']=product_option # 商品选项
       # 商品店铺 京东自营没有店铺名
       # shop=jsonpath(response_json,'$..shop')
       shop=response_json['wareInfo']['shopInfo']['shop']
       if shop:
           item['product_shop'] ={
               'shop_id':shop['shopId'],
               'shop_name':shop['name'],
               'shop_score': shop['score'],
           }
       else:
           item['product_shop']={
       'shop_name':'京东自营店',
       }
       product_category_id =response_json['wareInfo']['basicInfo']['category']  # 商品类别ID
       #category: "737;794;798" 因替换为 category: "737,794,798"
       item['product_category_id'] = product_category_id.replace(';',',')
       # print(item)
       #准备促销信息的URL
       ad_url='https://cd.jd.com/promotion/v2?skuId={}&area=17_1381_50712_0&cat={}'.format(item['product_sku_id'],item['product_category_id'])
       #构建促销信息的请求
       yield scrapy.Request(ad_url,callback=self.parse_product_ad,meta={'item':item})

    def parse_product_ad(self,response):
        item=response.meta['item']
        response_json=json.loads(response.body.decode('GBK'))#把数据转化成字典
        item['product_ad']=jsonpath(response_json,'$..ad')[0] if jsonpath(response_json,'$..ad') else ''
        #准备评价信息URL 构建评价信息的请求
        comments_url='https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}'.format(item['product_sku_id'])
        yield scrapy.Request(comments_url,callback=self.parse_product_comments,meta={'item':item})
    def parse_product_comments(self,response):
        item = response.meta['item']
        response_json = json.loads(response.text)  # 把数据转化成字典
        # print(response_json)
        item['product_comments']= {
           'CommentCount': response_json['CommentsCount'][0]['CommentCount'],
           'GoodCount': response_json['CommentsCount'][0]['GoodCount'],
            'PoorCount': response_json['CommentsCount'][0]['PoorCount'],
            'GoodRate':response_json['CommentsCount'][0]['GoodRate']
        }  # 商品评论数量
        #构建价格请求
        price_url='https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['product_sku_id'])
        yield scrapy.Request(price_url,callback=self.parse_product_price,meta={'item':item})
    def parse_product_price(self,response):
        item = response.meta['item']
        response_json = json.loads(response.text)  # 把数据转化成字典
        item['product_price']= response_json[0]['p']  # 商品价格
        yield item