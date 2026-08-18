import requests
import re
import random


def GET_QQW(region, prefix):
    number_sg = f"{region}{prefix}"
    url = f"https://telphone.cn/prefix/{number_sg}/"
    response = requests.get(url)
    if response.status_code != 200:
        return
    html_content = response.text
    pattern = re.compile(r'<a href="/prefix/(\d{7})/">([\d]+)号段')
    matches = pattern.findall(html_content)
    numSG_list = [match[1] for match in matches]
    return numSG_list


def QQW(pattern, numSG_list):
    regex_pattern = pattern.replace('x', '\\d')
    return [num for num in numSG_list if re.fullmatch(regex_pattern, num)]


def HSW(pattern):
    suffixes = [f'{i:04d}' for i in range(10000)]
    regex_pattern = pattern.replace('x', '\\d')
    return [suffix for suffix in suffixes if re.fullmatch(regex_pattern, suffix)]


def main():
    phonex = input('输入模糊手机号,x为未知位,注意前三位不能模糊!\n  >')
    region = input('输入地区\n  >')
    numSG_list = GET_QQW(region, phonex[:3])
    numSG_input = phonex[:7]
    matched_numSG = QQW(numSG_input, numSG_list)
    suffix_input = phonex[7:]
    matched_suffixes = HSW(suffix_input)
    numberphone = []
    with open('phone.txt', 'w') as f:
        for qqw in matched_numSG:
            for hsw in matched_suffixes:
                f.write(qqw + hsw + "\n")
    with open('phone.vcf', 'w') as f:
        for qqw in matched_numSG:
            for hsw in matched_suffixes:
                phone = qqw + hsw
                vcf_entry = f"BEGIN:VCARD\nVERSION:3.0\nN:;{phone};;;\nFN:{phone}\nTEL;type=CELL;type=VOICE;type=pref:{phone}\nEND:VCARD\n"
                f.write(vcf_entry)
    print('手机号以及VCF文件已经保存到 phone.txt 与 phone.vcf 文件中了！')


if __name__ == '__main__':
    main()
