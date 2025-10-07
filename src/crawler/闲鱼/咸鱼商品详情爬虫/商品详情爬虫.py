from pprint import pprint

import requests

headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "t=333d89bdd8d3c7f1680d61c314977359; tracknick=tb575736359; cna=5dFRIU3sMHMBASQJijx6xuFX; isg=BA4O1Z6E6rPx1V7kM_eYllnfX-TQj9KJBFr77zhXA5HMm671oBaHmbdQ18f3hsqh; havana_lgc2_77=eyJoaWQiOjIyMDk5NjgxNDA2MTcsInNnIjoiZjhjNTRhYmNkNWYyM2RiNzIzZTcxYTUxYTUyOWExZGYiLCJzaXRlIjo3NywidG9rZW4iOiIxbkFmbUpERllVQzhoamJuVVBEVjdZdyJ9; _hvn_lgc_=77; havana_lgc_exp=1760719611057; mtop_partitioned_detect=1; _m_h5_tk=d600392e8884098f2d0b81b17c792cdc_1759801420552; _m_h5_tk_enc=748cb5f548dd2a1f2a4a2208fd29dd1d; cookie2=1bd479bb51a7304737dd39912bcce0eb; _samesite_flag_=true; sgcookie=E100lSj5ts%2Bd9eb0HAVpdFmW%2BsVh9FYgXvUZuwcDxh0BtMKbwlSXJGs5OlNCOdjXKrrUB4oRAn7SpNlLypY%2BSmUclm%2Fn0PN6lsfI%2FDaqY7Dmno6l%2F5%2BZX8Jlqq1URukGipG2; csg=2de4d3fd; _tb_token_=3f65e75e137d5; unb=2209968140617; sdkSilent=1759879902293; xlly_s=1; tfstk=gtGjLTa-UijXnVDLh58PFgHEtdN68URFfNat-VCVWSFAXG3L4mr4gFA_Xmqrgou4MCatY0i_IEqaXliZWx8yTBumo5Vt1HReTluQMfifDRF9W_U08UzAFKYGm5V9Y3WP6-AQsmhUoD2tyUaa71BxXrd-yu4_WZnTD8I8RyVTXcnTwuUaSiUT6tIRwu4T61nT6UN8qPNTXcF9P4hkwgawhP3XJqxB6nv5pqr561h7yhqtlBf3kj4XSl0zVh-ZNiebvqE56ndhxfE_qXKyF4mZHmzofBt79vmS1JF6GM4je2N80WdAwSlmkvet9hXtoSqbwjHCW137GueSG-jXVkhmyXV8UBLIybmqobgNWCUrYu3mM5Op-SNYD7ao_3fYfYHtg-VGDhZiN4hxCgP5TkwQAO_7K1a7YUT5IObY8fKd3C4AF-UukB8WPg6gHz47YUT5IO2YrrHePUs5I",
    "origin": "https://www.goofish.com",
    "priority": "u=1, i",
    "referer": "https://www.goofish.com/",
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

url = "https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/"
data_form = {
    'data': '{"itemId": "963567908521"}'
}
# 查询参数
params = {
    "jsv": "2.7.2",
    "appKey": "34839810",
    "t": "1759793614723",
    "sign": "2f84c8f1628ea3253f8343def6720c7c",
    "v": "1.0",
    "type": "originaljson",
    "accountSite": "xianyu",
    "dataType": "json",
    "timeout": "20000",
    "api": "mtop.taobao.idle.pc.detail",
    "sessionOption": "AutoLoginOnly",
    "spm_cnt": "a21ybx.item.0.0",
    "spm_pre": "a21ybx.search.searchFeedList.1.1b4a1c13dDFwro",
    "log_id": "1b4a1c13dDFwro"
}
response = requests.post(url, headers=headers, params=params, data=data_form)
resjson = response.json()
pprint(resjson)
