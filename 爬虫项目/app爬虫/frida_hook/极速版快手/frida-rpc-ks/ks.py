import requests,time,json
import hook

def download_video(url, video_id):
    detail_header = {
        'Accept-Encoding': 'identity',
        'User-Agent': 'okhttp/3.10.0.1 vpwp/',
        'Connection': 'keep-alive',
    }
    print('download video')
    r = requests.get(url=url, verify=False, headers=detail_header)
    print(r.status_code)
    with open('D:/code/test_decompile/dy/{}.mp4'.format(video_id),'wb') as f:
        f.write(r.content)

def download_req(url):
    channel_header = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'com.ss.android.ugc.aweme.lite/203 (Linux; U; Android 6.0; zh_CN; Nexus 6P; Build/MDA89D; Cronet/58.0.2991.0)',
    'Connection': 'keep-alive',
    'Host': 'aweme.snssdk.com'
    }
    r = requests.get(url=url, verify=False, headers=channel_header)
    print(r.status_code)
    return r.text

def start():

    #'https://aweme.snssdk.com/aweme/v1/challenge/aweme/?ch_id=1649450080661508&query_type=0&cursor=20&count=20&type=5&retry_type=no_retry&iid=91658564592&device_id=69852570923&ac=wifi&channel=xiaomi&aid=2329&app_name=douyin_lite&version_code=203&version_name=2.0.3&device_platform=android&ssmix=a&device_type=Nexus+6P&device_brand=google&language=zh&os_api=23&os_version=6.0&openudid=dd08f504420bcde0&manifest_version_code=203&resolution=1440*2392&dpi=560&update_version_code=2030&_rticket=1573385459665&ts=1573385457&as=aad341fde85dc7f4f3d341&cp=fe38d341fde8d341fe3032&mas=01199323991959b313f319b9b985dc10f0b313f319f3591359d3f9'
    crawl_url = 'https://aweme.snssdk.com/aweme/v1/challenge/aweme/?ch_id=1649450080661508&query_type=0&cursor=20&count=20&type=5&retry_type=no_retry&iid=91658564592&device_id=69852570923&ac=wifi&channel=xiaomi&aid=2329&app_name=douyin_lite&version_code=203&version_name=2.0.3&device_platform=android&ssmix=a&device_type=Nexus+6P&device_brand=google&language=zh&os_api=23&os_version=6.0&openudid=dd08f504420bcde0&manifest_version_code=203&resolution=1440*2392&dpi=560&update_version_code=2030&_rticket=1573385459665&ts=1573385457'
    script = hook.prepare_hook()

    timestamp_w = time.time()
    timestamp = int(timestamp_w)
    device_id = 69852570923
    infos = ['sdk_version', '1.3.0', 'ts', str(timestamp), 'app_type', 'lite', 'os_api', '23', 'device_type', 'Nexus 6P',
    'device_platform', 'android', 'ssmix', 'a', 'iid', '91658564592', 'manifest_version_code', '203', 'dpi', '560',
    'version_code', '203', 'app_name', 'douyin_lite', 'version_name', '2.0.3', 'openudid', 'dd08f504420bcde0',
    'device_id', str(device_id), 'resolution', '1440*2392', 'os_version', '6.0', 'language', 'zh', 'device_brand', 'google',
    'ac', 'wifi', 'update_version_code', '2030', 'aid', '2329', 'channel', 'xiaomi', '_rticket', str(timestamp_w),
    'dwinfo', '5r_u5O7C8fL-_On08vO_p_Po8fGxv_zw_O3C8fL-_On08vO_p_Po8fGxv__87vjC7un86fTy87-n5r_-6O_v-PPpv6fmv-nk7fi_p62xv_D-_r-nrbG_8PP-v6etsb_5__C_p62xv_H8_r-nrbG__vjx8dT5v6etsb_-9Pm_p62xv-3u_r-nrbG_7-7u9L-nrbG___T5v6etsb_x_Om_p62xv_Hy8_r0v6etsb_z9Pm_p62xv-70-b-nrbG__-q_p62xv_70v6etsb_4_O_7_vO_p62xv-3-9L-nrbG_6fz-v6et4LG_8_j0-vX_8u_08_q_p8bA4LG_6vT79ML08_vyv6fG5r_q9Pv0wvP88Pi_p7_39Pzz-uf1_PP6v7G_6vT79MLw_P6_p7-t_qelr6erpaevpKeoqKeopb-xv-_u7vS_p7CopLG_9O7C_ujv7_jz6b-nrODAsb_--PHxv6fGwLG_8fL-_On08vPC8PL5-L-nrbG_8fL-_On08vPC7vjp6fTz-r-nrbG_7uj_8PTpwun08Pi_p6yoqq6pq6iupamlqK2xv73x_PP66Pz6-L-nv-f1sN7Tv7G_7fL07r-n8-jx8eA=']

    sig_url = 'https://iu.snssdk.com/location/locate/?sdk_version=1.3.0&ts={}&app_type=lite&os_api=23&device_type=Nexus 6P&device_platform=android&ssmix=a&iid=91658564592&manifest_version_code=203&dpi=560&version_code=203&app_name=douyin_lite&version_name=2.0.3&openudid=dd08f504420bcde0&device_id=69852570923&resolution=1440*2392&os_version=6.0&language=zh&device_brand=google&ac=wifi&update_version_code=2030&aid=2329&channel=xiaomi&_rticket={}'.format(timestamp, timestamp_w)

    sig = hook.get_sig(script, timestamp, sig_url, infos, str(device_id))

    print(crawl_url + sig)
    req_text = download_req(crawl_url + sig)

    data = json.loads(req_text)

    for i in data['aweme_list']:
        print('***video id/forward_count/play_count/digg_count/comment_count/share_count/download_count***')
        print('{}/{}/{}/{}/{}/{}/{}'.format(i['statistics']['aweme_id'],i['statistics']['forward_count'],\
        i['statistics']['play_count'],i['statistics']['digg_count'],i['statistics']['comment_count'],\
            i['statistics']['share_count'], i['statistics']['download_count']))

        download_video(i['video']['play_addr']['url_list'][0], i['statistics']['aweme_id'])
start()