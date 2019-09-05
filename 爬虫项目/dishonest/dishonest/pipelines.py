# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
drop table if exists dishonest; -- 如果表存在就删除
-- 创建表
create table dishonest(
dishonest_id INT NOT NULL AUTO_INCREMENT, -- id主键
age INT NOT NULL, -- 年龄，自然人年龄都大于0,企业等于0
name VARCHAR(200) NOT NULL,  -- 失信人名称
sexy VARCHAR(50) NOT NULL, -- 性别
card_num VARCHAR(50), -- 失信人号码
area VARCHAR(50) NOT NULL, -- 区域
content VARCHAR(2000) NOT NULL, -- 失信内容
business_entity VARCHAR(20), -- 企业法人
publish_date VARCHAR(20), -- 发布时间
publish_unit VARCHAR(200), -- 发布单位
update_date DATETIME, -- 创建日期
PRIMARY KEY (dishonest_id)
);
"""
"""
实现管道类
步骤：
1，open_spider中，建立数据库连接，获取操作的数据的cursor
2,在close_spider中，关闭cursor,关闭数据库链接
3，在process_item中，如果数据不存，保存数据
"""
import pymysql
class DishonestPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.Connect(host="localhost", port=3306, user="hao", passwd="4786874", db="dishonest", charset="utf8")
        #获取操作数据库的cursor
        self.cursor=self.db.cursor()

    def close_spider(self,spider):
        #在close_spider中，关闭cursor,关闭数据库连接
        # 1，先关闭cursor
        self.cursor.close()
        #2,在关闭数据库连接
        self.db.close()
    def process_item(self, item, spider):
        #在process_item中，如果数据不存，保存数据
        #如果是自然人，根据证件号进行判断
        #如果是企业/组织：企业名称 和 区域进行判断
        #如何判断是企业还是自然人，如果年龄为0就是企业，否则是自然人
        if item['age']==0:
            #如果是企业，根据企业名称和区域进行判断 是否重复
            select_count_sql="SELECT COUNT(1) from dishonest WHERE name = '{}' and area='{}'".format(item['name'],item['area']) #查询sql库'name，area 数量为1
        else:
            card_num=item['card_num']
            #如果证件号是18位，那么倒数第七位和倒数第四位（不包含），三个数字使用****替换
            if len(card_num) ==18:
                card_num=card_num.replace(card_num[-8:-4],'****')
                print(card_num,len(card_num))
                #为了保护失信人隐私 和数据一致，把修改的数据赋予回去
                item['card_num']=card_num

            #否则就是自然人
            select_count_sql="SELECT COUNT(1) from dishonest WHERE card_num ='{}'".format(item['card_num'])
        #执行查询SQL
        self.cursor.execute(select_count_sql)
        #获取查询结果
        count=self.cursor.fetchone()[0]
        if count ==0:
            keys,values =zip(*dict(item).items()) #dict(item).items()整合成列表性元组，zip拆分列表成各个元组，keys,values接收元组的键和值
            # 如果没有数据，就插入数据
            insert_sql='INSERT INTO dishonest ({}) VALUES ({})'.format(','.join(keys),','.join(['%s'] * len(keys))
                                                                       )
            #执行SQL
            self.cursor.execute(insert_sql,values)
            #提交事务
            self.db.commit()
            spider.logger.info('插入数据')

        else:
            #否则就重复了
            spider.logger.info('数据重复')

        return item
