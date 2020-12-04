import time, json
from mitmproxy import ctx
def response(flow):
    url = 'https://r.inews.qq.com/getQQNewsComment?'  # 评论所在的链接（较完整）
    url = 'https://r.inews.qq.com'  # 评论所在的链接（较完整）
    text= flow.response.text
    data = json.loads(text)
    # print("输出：",data)
    # request = flow.request
    # info = ctx.log.info #输出打印
    # info(str(request.headers))
    # info(str(request.cookies))
    # info(request.host)
    # info(request.method)
    # info(str(request.port))
    # info(request.scheme)
    # print("配置信息",info)
    if url in flow.request.url:
        text = flow.response.text
        data = json.loads(text)
        print("打印",data)
        # 从Charles中观测，data是个列表对象，列表对象是没有get()方法的，因此需提取出字典
        data = data.get('comments').get('new')

        if data:  # 判断对象是否为空，data是评论集，包含多个评论
            for item in data:  # 处理每一条评论，此时item是列表
                item = item[0]  # 将列表转化为字典，从Charles中观测为嵌套字典的列表

                # 获取评论的信息
                nick = item.get('nick')  # 昵称
                agree = item.get('agree_count')  # 点赞数
                sex = item.get('sex')  # 性别
                reply_num = item.get('reply_num')  # 互动数
                city = item.get('province_city')  # 所在城市
                comment = item.get('reply_content')  # 评论
                # 时间戳的转换
                date = time.strftime("%Y-%m-%d", time.localtime(item.get('pub_time')))
                print(nick, agree, reply_num, sex, city, comment, date)

                # 获取子评论
                data = item.get('reply_list')  # 嵌套字典的列表，包含多个子评论
                if data:  # 判断对象是否为空，data是子评论集，包含多个子评论
                    for item2 in data:
                        item2 = item2[0]  # 提取出字典
                        reply_date = time.strftime("%Y-%m-%d", time.localtime(item2.get('pub_time')))
                        reply_nick = item2.get('nick')
                        reply_agree = item2.get('agree_count')
                        reply_sex = item2.get('sex')
                        reply_city = item2.get('province_city')
                        reply_comment = item2.get('reply_content')
                        print(reply_date, reply_nick, reply_agree, reply_sex, reply_city, reply_comment)