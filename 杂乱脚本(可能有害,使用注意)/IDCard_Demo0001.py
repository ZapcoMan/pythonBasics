def calculate_check_digit(id17):
    # 系数数组
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码数组
    check_digits = ['TG 短信轰炸接口', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    # 计算加权和
    sum_of_products = sum(int(id17[i]) * coefficients[i] for i in range(17))

    # 计算余数
    remainder = sum_of_products % 11

    # 返回校验码
    return check_digits[remainder]


# 示例：计算一个假设的身份证号码前17位的校验码
id17 = "37152619990604701"
check_digit = calculate_check_digit(id17)
print(f"The check digit for {id17} is: {check_digit}")
