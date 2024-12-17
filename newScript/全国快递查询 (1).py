import requests
import json

anchun_kdh = input('需要查询的快递单号:')

api_url = f"http://api.yujn.cn/api/kuaidi.php?type=json&id={anchun_kdh}"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    print("快递信息：")
    for index, item in enumerate(data['data'], start=1):
        print(f"信息 {index}:")
        print(f"时间：{item['time']}")
        print(f"状态：{item['context']}")
        print(f"地点：{item['location']}")
        print("-" * 52)
else:
    print("请求失败，状态码：", response.status_code)
    
    print('程序制作者:@anchun_cn')
print('频道:@qq_cncom')
#'频道:@qq_cncom'😭
#禁止用此脚本参与违法行为.