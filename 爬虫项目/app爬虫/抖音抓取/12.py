import requests,time
t=round(time.time())
print(t)
def handel_requests():
    url="https://aweme.snssdk.com/aweme/v1/user/profile/other/?sec_user_id=MS4wLjABAAAAsQlhqcUg3uBNzJjNnf3Ngndgx8-MHWswKkEeJNIlrGY&address_book_access=1&from=0&publish_video_strategy_type=2&user_avatar_shrink=188_188&user_cover_shrink=750_422&os_api=22&device_type=LIO-AN00&ssmix=a&manifest_version_code=130701&dpi=160&uuid=866174168757686&app_name=aweme&version_name=13.7.0&ts=1606825938&cpu_support64=false&app_type=normal&appTheme=dark&ac=wifi&host_abi=armeabi-v7a&update_version_code=13709900&channel=tengxun_new&_rticket=1606825939701&device_platform=android&iid=4098619052668413&version_code=130700&cdid=929ad0da-7ac8-43a7-b9f0-2232b0644376&openudid=71f86ee34624e058&device_id=835268664374951&resolution=540*960&os_version=5.1.1&language=zh&device_brand=HUAWEI&aid=1128&mcc_mnc=46007"
    headers={
        "Accept-Encoding":"gzip",
"passport-sdk-version":"18",
"X-Tt-Token":"0096e3fa92e103c8251390195aa717092905c17617b39447ae19652014c431843ed313b2b1f2356c2c4e3d69f2d85d6c315a8c6423f6bbce790efc6c4d0f26c6f8da08ca31ce3048ab208d28c0baee86084c9-1.0.0",
"sdk-version":"2",
"X-SS-REQ-TICKET":"1606924649961",
# "Cookie":"install_id=4098619052668413; ttreq=1$31cadc582c563463bc3408599ad8380c68b5fa27; passport_csrf_token=b3045264b38770ed528d845e563c3b9f; d_ticket=af94999acdff7a465b9d8ba06e838ad1fd5e2; multi_sids=1059558310549672%3A96e3fa92e103c8251390195aa7170929; odin_tt=277a0ace0dd087e490b94135922d6d5ea58ff553c9bede174d93798e13826cb49f85eb2356ab3099722cb40cdc353a085af91d9c11a9568937e5ee7f426f7057; n_mh=seWLwL85jKlm0SYqdrZyCUoglY2Z9y9odDsaJHwoX1M; sid_guard=96e3fa92e103c8251390195aa7170929%7C1606822332%7C5184000%7CSat%2C+30-Jan-2021+11%3A32%3A12+GMT; uid_tt=dd755e3bcac67c623c729b50d911ed7b; uid_tt_ss=dd755e3bcac67c623c729b50d911ed7b; sid_tt=96e3fa92e103c8251390195aa7170929; sessionid=96e3fa92e103c8251390195aa7170929; sessionid_ss=96e3fa92e103c8251390195aa7170929",
"X-Khronos":"1606825939",
"X-Gorgon":"040420220001fd1fbe8e0a37d39f7502eb1c186a64c7e313cc51",
"Host":"aweme.snssdk.com",
"Connection":"Keep-Alive",
"User-Agent":"okhttp/3.10.0.1",
    }
    # #添加代理
    # proxies=get_porpy()
    # response = requests.post(url=url, headers=headers, data=data,proxies=)
    #不添加代理
    response = requests.post(url=url,headers=headers)
    print(response.text)

# handel_requests()

def handel_requests():
    url="https://aweme.snssdk.com/aweme/v2/feed/?type=0&max_cursor=0&min_cursor=-1&count=6&volume=0.73&pull_type=2&need_relieve_aweme=0&filter_warn=0&req_from&is_cold_start=0&longitude=112.57011578147775&latitude=40.00222203983785&address_book_access=1&gps_access=1&cached_item_num=3&last_ad_show_interval=-1&mac_address=00%3A15%3A5D%3A60%3AD4%3A8F&preload_aweme_ids&download_sdk_info=%7B%22space_unoccupied%22%3A57597832%7D&action_mask=-1&action_mask_detail=%7B%226901965446648499459%22%3A1%2C%226898979573099138312%22%3A128%2C%226891220748946492676%22%3A0%2C%226897433676863360271%22%3A0%7D&teen_protector_vote_aweme_count=0&last_teen_protector_vote_aweme_interval=0&sp=2490&is_order_flow=0&user_avatar_shrink=96_96&screen_type=0&need_personal_recommend=1&live_auto_enter=0&os_api=22&device_type=LIO-AN00&ssmix=a&manifest_version_code=130701&dpi=160&uuid=866174168757686&app_name=aweme&version_name=13.7.0&ts=1607000133&cpu_support64=false&app_type=normal&appTheme=dark&ac=wifi&host_abi=armeabi-v7a&update_version_code=13709900&channel=tengxun_new&_rticket=1607000134416&device_platform=android&iid=4098619052668413&version_code=130700&cdid=263a0b79-88c9-405b-ba3f-7f89ca9b2b14&openudid=71f86ee34624e058&device_id=835268664374951&resolution=540*960&os_version=5.1.1&language=zh&device_brand=HUAWEI&aid=1128&mcc_mnc=46007"
    headers={
    "Accept-Encoding":"gzip",
"passport-sdk-version":"18",
"X-Tt-Token":"00bcd89aecb7d4173d41b10f0c0034802e0318aa413b441b9dc0b0993bc570674a79a93024137bc3795941cd768dfb7ea245c23774178ddffd0f31ee1c2ca130203838dc0a1eafd52ed387b558f733799b65b-1.0.0",
"sdk-version":"2",
"X-SS-REQ-TICKET":"1607000134428",
"Cookie":"install_id=4098619052668413; ttreq=1$31cadc582c563463bc3408599ad8380c68b5fa27; passport_csrf_token=d163f6f0e3579420c242dc0321be2a6c; d_ticket=7f6c0ff62ae5708f63eaa6344afc2e89fd5e2; multi_sids=1059558310549672%3Abcd89aecb7d4173d41b10f0c0034802e; odin_tt=cdd897f512424ec89144cd1eeb6c1f40683b7da550bf916ff058719a76d01b6a53c90cfc12a34b4394c7b213168b2b45fd87749de1f4dd495e172e0177d14820; n_mh=seWLwL85jKlm0SYqdrZyCUoglY2Z9y9odDsaJHwoX1M; sid_guard=bcd89aecb7d4173d41b10f0c0034802e%7C1606983874%7C5184000%7CMon%2C+01-Feb-2021+08%3A24%3A34+GMT; uid_tt=92405f958c33cade617c8ef310fe787e; uid_tt_ss=92405f958c33cade617c8ef310fe787e; sid_tt=bcd89aecb7d4173d41b10f0c0034802e; sessionid=bcd89aecb7d4173d41b10f0c0034802e; sessionid_ss=bcd89aecb7d4173d41b10f0c0034802e",
"X-Khronos":"1607000134",
"X-Gorgon":"0404c08f0001f108de2091be36c4888974e19483a65a175c5205",
"Host":"aweme.snssdk.com",
"Connection":"Keep-Alive",
"User-Agent":"okhttp/3.10.0.1",


}
    # #添加代理
    # proxies=get_porpy()
    # response = requests.post(url=url, headers=headers, data=data,proxies=)
    #不添加代理
    response = requests.get(url=url,headers=headers)
    print(response.text)

handel_requests()