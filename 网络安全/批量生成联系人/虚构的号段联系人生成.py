import random
import uuid
from datetime import datetime, timedelta

# 常见姓氏
common_surnames = [
    "赵","钱","孙","李","周","吴","郑","王","冯","陈","褚","卫","蒋","沈","韩","杨","朱","秦","尤","许",
    "何","吕","施","张","孔","曹","严","华","金","魏","陶","姜","戚","谢","邹","喻","柏","水","窦","章",
    "云","苏","潘","葛","奚","范","彭","郎","鲁","韦","昌","马","苗","凤","花","方","俞","任","袁","柳",
    "酆","鲍","史","唐","费","廉","岑","薛","雷","贺","倪","汤","滕","殷","罗","毕","郝","邬","安","常",
    "乐","于","时","傅","皮","卞","齐","康","伍","余","元","卜","顾","孟","平","黄","和","穆","萧","尹",
    "姚","邵","湛","汪","祁","毛","禹","狄","米","贝","明","臧","计","伏","成","戴","谈","宋","茅","庞",
    "熊","纪","舒","屈","项","祝","董","梁","杜","阮","蓝","闵","席","季","麻","强","贾","路","娄","危",
    "江","童","颜","郭","梅","盛","林","刁","钟","徐","邱","骆","高","夏","蔡","田","樊","胡","凌","霍",
    "虞","万","支","柯","咎","管","卢","莫","经","房","裘","缪","干","解","应","宗","宣","丁","贲","邓",
    "郁","单","杭","洪","包","诸","左","石","崔","吉","钮","龚","程","嵇","邢","滑","裴","陆","荣","翁",
    "荀","羊","於","惠","甄","曲","家","封","芮","羿","储","靳","汲","邴","糜","松","井","段","富","巫",
    "乌","焦","巴","弓","牧","隗","山","谷","车","侯","宓","蓬","全","郗","班","仰","秋","仲","伊","宫",
    "宁","仇","栾","暴","甘","钭","厉","戎","祖","武","符","刘","景","詹","束","龙","叶","幸","司","韶",
    "郜","黎","蓟","薄","印","宿","白","怀","蒲","邰","从","鄂","索","咸","籍","赖","卓","蔺","屠","蒙",
    "池","乔","阴","郁","胥","能","苍","双","闻","莘","党","翟","谭","贡","劳","逄","姬","申","扶","堵",
    "冉","宰","郦","雍","郤","璩","桑","桂","濮","牛","寿","通","边","扈","燕","冀","郏","浦","尚","农",
    "温","别","庄","晏","柴","瞿","阎","充","慕","连","茹","习","宦","艾","鱼","容","向","古","易","慎",
    "戈","廖","庾","终","暨","居","衡","步","都","耿","满","弘","匡","国","文","寇","广","禄","阙","东",
    "欧","殳","沃","利","蔚","越","夔","隆","师","巩","厍","聂","晁","勾","敖","融","冷","訾","辛","阚",
    "那","简","饶","空","曾","毋","沙","乜","养","鞠","须","丰","巢","关","蒯","相","查","后","荆","红",
    "游","竺","权","逯","盖","益","桓","公","万俟","司马","上官","欧阳","夏侯","诸葛","闻人","东方",
    "赫连","皇甫","尉迟","公羊","澹台","公冶","宗政","濮阳","淳于","单于","太叔","申屠","公孙","仲孙",
    "轩辕","令狐","钟离","宇文","长孙","慕容","鲜于","闾丘","司徒","司空","亓官","司寇","仉督","子车",
    "颛孙","端木","巫马","公西","漆雕","乐正","壤驷","公良","拓跋","夹谷","宰父","谷梁","晋楚","闫法",
    "汝鄢","涂钦","段干","百里","东郭","南门","呼延","归海","羊舌","微生","岳帅","缑亢","况郈","有琴",
    "梁丘","左丘","东门","西门","商牟","佘佴","伯赏","南宫","墨哈","谯笪","年爱","阳佟","第五","言福"
]


# 常见男性名字
male_names = [
    "伟", "芳", "勇", "艳", "杰", "涛", "明", "超", "强", "磊",
    "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀英",
    "霞", "平", "刚", "桂英", "鹏", "红", "华", "亮", "宁", "波",
    "丹", "建华", "静", "洁", "晶", "凯", "丽娟", "玲", "龙", "梅",
    "楠", "倩", "琴", "荣", "霞", "晓", "燕", "颖", "志强", "俊",
    "斌", "浩", "然", "博", "锐", "健", "峰", "磊", "洋", "宇",
    "翔", "聪", "智", "勇", "涛", "源", "凯", "鑫", "帅", "林"
]

# 常见女性名字
female_names = [
    "伟", "芳", "娜", "敏", "静", "丽", "秀英", "霞", "桂英", "艳",
    "娟", "红", "丽娟", "玲", "丹", "秀兰", "秀珍", "秀芳", "婷", "玉兰",
    "梅", "洁", "晶", "丽丽", "霞", "秀云", "秀梅", "丽华", "琴", "丽萍",
    "秀英", "丽娜", "丽娟", "秀霞", "丽琴", "秀兰", "丽红", "丽梅", "丽芳", "秀珍",
    "莹", "媛", "倩", "悦", "瑶", "琳", "娜", "婷", "雪", "慧",
    "妍", "丽", "倩", "燕", "红", "丽", "艳", "丽", "娟", "莉"
]

# 家庭关系
family_relations = {
    "爸爸": {"gender": "male", "min_age": 30, "max_age": 70},
    "妈妈": {"gender": "female", "min_age": 30, "max_age": 70},
    "爷爷": {"gender": "male", "min_age": 60, "max_age": 90},
    "奶奶": {"gender": "female", "min_age": 60, "max_age": 90},
    "外公": {"gender": "male", "min_age": 60, "max_age": 90},
    "外婆": {"gender": "female", "min_age": 60, "max_age": 90},
    "大伯": {"gender": "male", "min_age": 30, "max_age": 70},
    "二伯": {"gender": "male", "min_age": 30, "max_age": 70},
    "三伯": {"gender": "male", "min_age": 30, "max_age": 70},
    "叔叔": {"gender": "male", "min_age": 25, "max_age": 65},
    "舅舅": {"gender": "male", "min_age": 25, "max_age": 65},
    "姑姑": {"gender": "female", "min_age": 25, "max_age": 65},
    "姨": {"gender": "female", "min_age": 25, "max_age": 65},
    "表哥": {"gender": "male", "min_age": 18, "max_age": 40},
    "表弟": {"gender": "male", "min_age": 5, "max_age": 30},
    "表妹": {"gender": "female", "min_age": 5, "max_age": 30},
    "堂哥": {"gender": "male", "min_age": 18, "max_age": 40},
    "堂姐": {"gender": "female", "min_age": 18, "max_age": 40},
    "堂弟": {"gender": "male", "min_age": 5, "max_age": 30},
    "堂妹": {"gender": "female", "min_age": 5, "max_age": 30},
    "表姐": {"gender": "female", "min_age": 18, "max_age": 40},
    "嫂子": {"gender": "female", "min_age": 25, "max_age": 50},
    "姐夫": {"gender": "male", "min_age": 25, "max_age": 50},
    "妹夫": {"gender": "male", "min_age": 25, "max_age": 45},
    "姐姐": {"gender": "female", "min_age": 20, "max_age": 50},
    "妹妹": {"gender": "female", "min_age": 10, "max_age": 35},
    "哥哥": {"gender": "male", "min_age": 20, "max_age": 50},
    "弟弟": {"gender": "male", "min_age": 10, "max_age": 35}
}

# 职业和部门
positions = ["主任", "局长", "科长", "总监", "老板", "董事长", "经理", "主管", "工程师", "会计", "出纳", "文员",
            "医生", "护士", "教师", "律师", "建筑师", "设计师", "程序员", "销售", "客服", "司机", "厨师", "保安"]
departments = ["财务部", "人事部", "办公室", "政工处", "宣传部", "后勤科", "市政", "工商局", "教育局", "开发组",
              "技术部", "销售部", "市场部", "客服部", "研发部", "运营部", "采购部", "质检部", "生产部", "行政部"]

# 同事关系
colleague_relations = ["同事", "合作伙伴", "客户", "供应商", "下属", "助理"]

# 朋友关系
friend_relations = ["朋友", "同学", "战友", "邻居", "老乡", "球友", "网友", "校友"]

# 服务人员关系
service_relations = ["快递员", "外卖员", "物业管理员", "保安", "保洁", "维修工", "理发师", "医生", "护士", "老师"]

# 虚拟手机号段（避免与现实中使用的号码冲突）
fake_phone_prefixes = [
    "170", "171", "162", "165", "167",  # 虚拟运营商号段
    "190", "192", "193", "195", "197",  # 较少使用的号段
    "134", "135", "136", "137", "138"   # 部分真实号段（用于混合）
]

# 城市列表
cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "苏州", "武汉", "成都", "重庆",
          "天津", "西安", "青岛", "大连", "厦门", "宁波", "无锡", "郑州", "长沙", "福州",
          "济南", "沈阳", "哈尔滨", "长春", "石家庄", "太原", "合肥", "南昌", "南宁", "昆明"]

# 公司名称前缀
company_prefixes = ["华为", "腾讯", "阿里巴巴", "百度", "京东", "小米", "美团", "滴滴", "字节跳动", "拼多多",
                   "中国银行", "工商银行", "建设银行", "农业银行", "平安保险", "中国移动", "中国联通", "中国电信",
                   "国家电网", "中石化", "中石油", "一汽", "上汽", "东风汽车", "长安汽车", "格力", "美的", "海尔"]

# 公司名称后缀
company_suffixes = ["科技有限公司", "贸易有限公司", "投资有限公司", "集团有限公司", "发展有限公司", "实业有限公司"]

# 学校名称
schools = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学", "南京大学", "中山大学", "华中科技大学",
           "北京理工大学", "北京航空航天大学", "哈尔滨工业大学", "西安交通大学", "电子科技大学", "中南大学", "华南理工大学",
           "第一中学", "第二中学", "实验中学", "外国语学校", "职业高中", "师范学校", "技术学院", "职业学院"]

# 邮箱后缀
email_suffixes = ["@qq.com", "@163.com", "@126.com", "@gmail.com", "@sina.com", "@sohu.com", "@hotmail.com"]

# 生成随机中文姓名
def generate_name(gender=None):
    """
    生成随机中文姓名

    Args:
        gender (str): 性别，'male' 或 'female'，如果为 None 则随机

    Returns:
        tuple: (姓名, 性别)
    """
    surname = random.choice(common_surnames)

    if gender is None:
        gender = random.choice(['male', 'female'])

    if gender == 'male':
        # 男性名字可能是一个或两个字
        if random.random() < 0.7:
            name_part = random.choice(male_names)
        else:
            name_part = random.choice(male_names) + random.choice(male_names)
    else:
        # 女性名字可能是一个或两个字
        if random.random() < 0.7:
            name_part = random.choice(female_names)
        else:
            name_part = random.choice(female_names) + random.choice(female_names)

    return surname + name_part, gender

# 生成不与现实中使用的手机号冲突的虚拟手机号码
def generate_phone():
    """
    生成虚拟的中国大陆手机号码，避免与现实中使用的号码冲突

    Returns:
        str: 11位虚拟手机号码
    """
    prefix = random.choice(fake_phone_prefixes)

    # 生成后8位数字
    suffix = "".join(random.choices("0123456789", k=8))

    # 为了进一步确保不与真实号码冲突，在特定位置使用特殊数字
    # 如在第4位数字固定为0或9
    suffix = suffix[:3] + random.choice(["0", "9"]) + suffix[4:]

    return prefix + suffix

# 生成邮箱地址
def generate_email(name):
    """
    根据姓名生成邮箱地址

    Args:
        name (str): 姓名

    Returns:
        str: 邮箱地址
    """
    # 使用姓名的拼音作为邮箱前缀（这里简化处理）
    pinyin_name = name.replace(name[0], name[0].lower(), 1)  # 姓氏小写
    for i in range(1, len(name)):
        pinyin_name += name[i]

    # 添加随机数字
    if random.random() < 0.5:
        pinyin_name += str(random.randint(1, 999))

    return pinyin_name + random.choice(email_suffixes)

# 生成公司名称
def generate_company():
    """
    生成随机公司名称

    Returns:
        str: 公司名称
    """
    prefix = random.choice(company_prefixes)
    if random.random() < 0.3:
        # 30%概率添加修饰词
        modifier = random.choice(["新", "大", "华", "中", "国", "东方", "南方", "北方"])
        prefix = modifier + prefix
    suffix = random.choice(company_suffixes)
    return prefix + suffix

# 生成生日（根据年龄）
def generate_birthday(age):
    """
    根据年龄生成生日

    Args:
        age (int): 年龄

    Returns:
        str: 生日，格式为 YYYY-MM-DD
    """
    current_year = datetime.now().year
    birth_year = current_year - age
    # 随机生成月份和日期
    birth_month = random.randint(1, 12)
    # 简化处理每月天数
    birth_day = random.randint(1, 28)
    return f"{birth_year}-{birth_month:02d}-{birth_day:02d}"

# 生成地址
def generate_address():
    """
    生成随机地址

    Returns:
        str: 地址
    """
    city = random.choice(cities)
    district = random.choice(["朝阳区", "海淀区", "西城区", "东城区", "丰台区", "石景山区", "浦东新区", "徐汇区", "长宁区", "静安区"])
    road = random.choice(["人民路", "解放路", "建设路", "发展路", "胜利路", "光明路", "幸福路", "和平路", "长江路", "黄河路"])
    number = str(random.randint(1, 500)) + random.choice(["号", "号院", "号楼"])
    detail = random.choice(["A座", "B座", "", "", ""])
    return city + district + road + number + detail

# 生成家庭联系人
def generate_family_contacts(count):
    """
    生成家庭联系人列表

    Args:
        count (int): 需要生成的家庭联系人数量

    Returns:
        list: 包含家庭联系人信息的列表
    """
    family_list = []
    relations = list(family_relations.keys())

    # 确保包含基本的直系亲属
    basic_relations = ["爸爸", "妈妈", "爷爷", "奶奶", "外公", "外婆"]
    for relation in basic_relations:
        if len(family_list) < count:
            family_list.append(relation)

    # 补充其他亲属
    while len(family_list) < count:
        family_list.append(random.choice(relations))

    return family_list[:count]

# 生成领导联系人
def generate_leader_contacts(count):
    """
    生成领导联系人列表

    Args:
        count (int): 需要生成的领导联系人数量

    Returns:
        list: 包含领导联系人信息的列表
    """
    leaders = []
    for _ in range(count):
        position = random.choice(positions)

        # 70% 概率加姓
        if random.random() < 0.7:
            surname = random.choice(common_surnames)
            leader_name = surname + position
        else:
            leader_name = position

        # 60% 概率加部门后缀
        if random.random() < 0.6:
            leader_name = leader_name + "-" + random.choice(departments)

        leaders.append(leader_name)
    return leaders

# 生成同事联系人
def generate_colleague_contacts(count):
    """
    生成同事联系人列表

    Args:
        count (int): 需要生成的同事联系人数量

    Returns:
        list: 包含同事联系人信息的列表
    """
    colleagues = []
    for _ in range(count):
        relation = random.choice(colleague_relations)
        surname = random.choice(common_surnames)

        # 80% 概率加职位或部门信息
        if random.random() < 0.8:
            if random.random() < 0.5:
                # 添加职位
                position = random.choice(positions)
                colleague_name = surname + relation + "(" + position + ")"
            else:
                # 添加部门
                department = random.choice(departments)
                colleague_name = surname + relation + "(" + department + ")"
        else:
            colleague_name = surname + relation

        colleagues.append(colleague_name)
    return colleagues

# 生成朋友联系人
def generate_friend_contacts(count):
    """
    生成朋友联系人列表

    Args:
        count (int): 需要生成的朋友联系人数量

    Returns:
        list: 包含朋友联系人信息的列表
    """
    friends = []
    for _ in range(count):
        relation = random.choice(friend_relations)
        surname = random.choice(common_surnames)
        friend_name = surname + relation
        friends.append(friend_name)
    return friends

# 生成服务人员联系人
def generate_service_contacts(count):
    """
    生成服务人员联系人列表

    Args:
        count (int): 需要生成的服务人员联系人数量

    Returns:
        list: 包含服务人员联系人信息的列表
    """
    services = []
    for _ in range(count):
        relation = random.choice(service_relations)
        surname = random.choice(common_surnames)

        # 50% 概率添加公司或机构信息
        if random.random() < 0.5:
            if relation in ["快递员", "外卖员", "维修工"]:
                company = generate_company()
                service_name = surname + relation + "(" + company + ")"
            elif relation in ["医生", "护士"]:
                hospital = random.choice(["人民医院", "中心医院", "第一医院", "协和医院", "华西医院"])
                service_name = surname + relation + "(" + hospital + ")"
            elif relation in ["老师"]:
                school = random.choice(schools)
                service_name = surname + relation + "(" + school + ")"
            else:
                service_name = surname + relation
        else:
            service_name = surname + relation

        services.append(service_name)
    return services

# 生成 vCard
vcf_entries = []
total_contacts = 1540
family_count = 300   # 家庭联系人数量
leader_count = 150   # 领导数量
colleague_count = 250 # 同事数量
friend_count = 200   # 朋友数量
service_count = 150  # 服务人员数量
random_count = total_contacts - family_count - leader_count - colleague_count - friend_count - service_count  # 随机联系人

# 生成家庭联系人vCard条目
family_relations_list = generate_family_contacts(family_count)
for relation in family_relations_list:
    name, gender = generate_name(family_relations[relation]["gender"])
    phone = generate_phone()
    age = random.randint(family_relations[relation]["min_age"], family_relations[relation]["max_age"])
    birthday = generate_birthday(age)
    email = generate_email(name)
    address = generate_address()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
relation};
FN:{name}({relation})
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成领导联系人vCard条目
for leader in generate_leader_contacts(leader_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(25, 65)
    birthday = generate_birthday(age)
    email = generate_email(name)
    address = generate_address()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
leader};
FN:{name}({leader})
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成同事联系人vCard条目
for colleague in generate_colleague_contacts(colleague_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(22, 60)
    birthday = generate_birthday(age)
    email = generate_email(name)
    address = generate_address()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
colleague};
FN:{name}({colleague})
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成朋友联系人vCard条目
for friend in generate_friend_contacts(friend_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(18, 55)
    birthday = generate_birthday(age)
    email = generate_email(name)
    address = generate_address()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
friend};
FN:{name}({friend})
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成服务人员联系人vCard条目
for service in generate_service_contacts(service_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(20, 65)
    birthday = generate_birthday(age)
    email = generate_email(name)
    address = generate_address()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;{
service};
FN:{name}({service})
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 生成随机姓名联系人vCard条目
for _ in range(random_count):
    name, gender = generate_name()
    phone = generate_phone()
    age = random.randint(18, 70)
    birthday = generate_birthday(age)
    email = generate_email(name)
    address = generate_address()
    uid = str(uuid.uuid4())
    entry = f"""BEGIN:VCARD
VERSION:3.0
N:{name};;;; 
FN:{name}
TEL;TYPE=CELL:{phone}
EMAIL:{email}
ADR:;;{address}
BDAY:{birthday}
UID:{uid}
END:VCARD"""
    vcf_entries.append(entry)

# 打乱联系人顺序
random.shuffle(vcf_entries)

# 拼接 vcf 内容
vcf_content = "\r\n".join(vcf_entries)

# 保存到文件
file_path = "C:/Users/Administrator/Desktop/Decontacts.vcf"
with open(file_path, "w", encoding="utf-8-sig") as f:
    f.write(vcf_content)

print("已生成:", file_path)
