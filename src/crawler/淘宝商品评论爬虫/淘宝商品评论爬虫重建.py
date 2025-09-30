import requests
import  re
import json
url = ('https://h5api.m.taobao.com/h5/mtop.taobao.rate.detaillist.get/6.0/?jsv=2.7.4&appKey=12574478&t=1759197367103&sign=e9f8bf5ab8b1d56e790015b88a2fb02a&'
       'api=mtop.taobao.rate.detaillist.get&v=6.0&isSec=0&ecode=1&timeout=20000&dataType=jsonp&valueType=string&type=jsonp&callback=mtopjsonp14&data=%7B%22showTrueCount%22%3Afalse%2C%22'
       'auctionNumId%22%3A%22979802405623%22%2C%22pageNo%22%3A1%2C%22pageSize%22%3A20%2C%22orderType%22%3A%22%22%2C%22searchImpr%22%3A%22-8%22%2C%22expression%22%3A%22%22%2C%22skuVids'
       '%22%3A%22%22%2C%22rateSrc%22%3A%22pc_rate_list%22%2C%22rateType%22%3A%22%22%7D')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Cookie': 't=1526546a8c63cfd36a5ceed67ca59dd5; thw=xx; cna=w6k1IRvSVwoBASQJijy/XNBW; wk_cookie2=1dbc251b612260ffc9a3de38a71ca72a; '
              'wk_unb=UUphw2zVrESuxidOHQ%3D%3D; _hvn_lgc_=0; havana_lgc2_0=eyJoaWQiOjIyMDk5NjgxNDA2MTcsInNnIjoiMjE0OTc1MWFlNzQ2NzUwNWUyYmMwMDg5YTgwMjA3ZjAiLCJzaXRlIjowLCJ0b2tlbiI6IjFuUkR4OTQ4UGFZZE9CTzhHWlZQNHZRIn0; '
              'lgc=tb575736359; cancelledSubSites=empty; tracknick=tb575736359; useNativeIM=false; wwUserTip=false; aui=2209968140617; cookie2=1a7764a92778e9951deae0d2b42a00f1; mtop_partitioned_detect=1; '
              '_m_h5_tk=fc39c54d0244c15db85794580a9ba528_1759204802161; _m_h5_tk_enc=c7b13b0394b06c956aa5f13a7910a4c3; sca=ae05147e; _m_h5_tk=843674fd7d878a303fa6d160a19afb9f_1759207685849; _m_h5_tk_enc=4b037f4e35d8144879665246f7d59e43; '
              '_samesite_flag_=true; sdkSilent=1759226049328; havana_sdkSilent=1759226049328; xlly_s=1; _tb_token_=3e115bd33747e; 3PcFlag=1759197330201; '
              'sgcookie=E100b4bFVvIS%2B26Eq5DFXxIXV%2FN%2BIyTo%2FfFa5od1xnkoaCAReZ8zjoWWSaxn0eXejw5jbAga4gOLN3h0utKgkK5jV0latcLBNs7h%2FLOBcNj3c8U%3D; '
              'cookie3_bak=1a7764a92778e9951deae0d2b42a00f1; cookie3_bak_exp=1759456534632; havana_lgc_exp=1790301334633; unb=2209968140617; '
              'uc1=existShop=false&cookie14=UoYbwhAxaxeNdQ%3D%3D&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&cookie21=WqG3DMC9FAJR1vdCtQ%3D%3D&pas=0; '
              'uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&id2=UUphw2zVrESuxidOHQ%3D%3D&nk2=F5RARU8g3KWi%2FM8%3D&vt3=F8dD2k66mOa6QJh8jJc%3D; csg=b4744f1c; env_bak=FM%2BgwZ4N3GOukL7Zx3w%2FhldIPUf0%2BKinyxc9I4jofGLC; '
              'cookie17=UUphw2zVrESuxidOHQ%3D%3D; dnk=tb575736359; skt=97e9fd6d47bbd043; existShop=MTc1OTE5NzMzNA%3D%3D; uc4=id4=0%40U2grGNOi4JMlBFrYt17VJWvbdEciCQVv&nk4=0%40FY4L6bwA%2BPjAWB5FIXzv6RUufB4XUQ%3D%3D; '
              '_cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=974; _nk_=tb575736359; cookie1=UNIFEIpeTKYn2woOqSU7ouObIDo3sVsD6bDqZzAUGHg%3D; isg=BObma_egsqoU22Z7u0Mx_a_1N1xoxyqBo7Q-a9CP8YnkU4dtOFMSkqBrr09ffCKZ; '
              'tfstk=gROtpYXI8DmiCDAO-FknirvllN336vYwJh87iijghHKpjU9GIEscMnKvDGXjb1AvvhYWIOYXiZOA_BvgiGmNMEtlM0moZbYw7_5jq0xuObIGNNQbhoj_RJ1ck625-JTw7szU-oMkdFzYCNZCGstfOM_V5swfCOgddabfG56b1JZCYM1fliw1de_5oZw6csgpRM7PGNtfC2LIwWuOYP_TMd'
              'wJAGQ8iAPYMBQOBiFcASdwO7X1V_jQGmJhW7SW5MFbGghapfLpScFy-1RD2axiO5KJlUJfpIEI2iRpRC9X8lnA6exww1O-X5bhTGWWh93s1eCOXtdAdz2F6KtwMOJTu48C1HJP4OMEYwdMZtIPpki6-eI1eKKiYSsMeetdEBq3Z_9yvIB5NgrkZQCZgujRoRgKJ-yVCw-mBJpVG0N26wIo5Ow43tbF'
              'Jg0KJ-yVCw7dqVN_3-Wc8'
}

response = requests.get(url, headers=headers).text
print(response)
match = re.search(r'mtopjsonp\d+\((.*)\)', response, re.S)
if match:
    json_str = match.group(1)
    data = json.loads(json_str)
    print(data["data"]["rateList"])
    # rateList = data["data"]["rateList"]
    # print(rateList)
else:
    print("不是标准 JSONP 格式")