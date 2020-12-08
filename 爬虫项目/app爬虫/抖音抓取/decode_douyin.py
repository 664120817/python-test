import json
from mitmproxy import ctx
from habdel_mongo import mongo_info
def response(flow):
    if "https://aweme.snssdk.com/aweme/v2/feed" in flow.request.url:  #原视频链接获取
        info = ctx.log.info
        info(flow.response.text)
        # print(flow.response.text,"888888888"*10)
        # print(flow.request.url)
    if "https://aweme.snssdk.com/aweme/v1/user/follower/list" in flow.request.url: #粉丝信息获取
        # with open('user.txt',"w")as f:
        #     f.write(flow.request.text)
        for user in json.loads(flow.response.text)['followers']:
            douyin_info={}
            douyin_info['uid']=user['uid']
            douyin_info['sec_uid'] = user['sec_uid']
            douyin_info['douyin_id'] = user['short_id']
            douyin_info['nickname'] = user['nickname']
            douyin_info['total_favorited'] = user['total_favorited']
            douyin_info['follower_count'] = user['follower_count']
            douyin_info['following_count'] = user['following_count']

            print(douyin_info)
            mongo_info.insert_item(douyin_info)