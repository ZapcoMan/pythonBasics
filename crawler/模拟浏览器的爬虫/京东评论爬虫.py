import json
from DrissionPage import ChromiumPage
import time

# 实例化浏览器对象
dp = ChromiumPage()

# 设置访问地址
Url = "https://item.jd.com/100076766489.html"

# 监听数据包
# 这里指定监听的URL是京东商品页面的评论接口，以便后续获取评论数据
dp.listen.start('https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments')

# 访问商品页面
dp.get(Url)

# 点击查看评论
# 通过CSS选择器定位到评论按钮并点击，以触发评论数据的加载
dp.ele('css:#detail > div.tab-main.large > ul > li:nth-child(5)').click()

# 初始化评论列表
all_comments = []

# 最大页数限制，防止无限循环
max_pages = 20
current_page = 0

while current_page < max_pages:
    # 等待数据包加载
    # 这里等待监听到的评论数据包加载完成，以便获取数据
    resp = dp.listen.wait()

    # 获取响应数据
    # 从监听到的数据包中提取评论的JSON数据
    json_data = resp.response.body

    # 解析JSON数据
    # 检查 json_data 的类型
    if isinstance(json_data, str):
        # 如果是字符串，则进行解析
        data = json.loads(json_data)
    elif isinstance(json_data, dict):
        # 如果已经是字典，则直接使用
        data = json_data
    else:
        # 其他类型，抛出异常
        raise TypeError("json_data 必须是 str 或 dict 类型")

    # 定义注释信息
    comments_info = {
        "id": "评论的唯一标识符",
        "guid": "用户的唯一标识符",
        "content": "评论的具体内容",
        "creationTime": "评论的创建时间",
        "isDelete": "评论是否被删除",
        "isTop": "评论是否置顶",
        "userImageUrl": "用户头像的URL",
        "topped": "是否置顶的标志",
        "replyCount": "评论的回复数量",
        "score": "评论的评分",
        "imageStatus": "图片状态",
        "usefulVoteCount": "有用投票的数量",
        "userClient": "用户使用的客户端类型",
        "discussionId": "评论的讨论ID",
        "imageCount": "评论中包含的图片数量",
        "anonymousFlag": "是否匿名",
        "plusAvailable": "用户的PLUS会员状态",
        "mobileVersion": "用户使用的手机版本",
        "images": "评论中包含的图片列表",
        "videos": "评论中包含的视频列表",
        "mergeOrderStatus": "合并订单状态",
        "productColor": "商品颜色",
        "productSize": "商品尺寸",
        "textIntegral": "文字积分",
        "imageIntegral": "图片积分",
        "ownId": "拥有者的ID",
        "ownType": "拥有者类型",
        "extMap": "扩展信息",
        "location": "用户位置",
        "status": "评论状态",
        "referenceId": "参考的商品ID",
        "referenceTime": "参考时间",
        "nickname": "用户昵称",
        "replyCount2": "回复数量（另一个计数）",
        "userImage": "用户头像",
        "orderId": "订单ID",
        "integral": "积分",
        "productSales": "商品销售信息",
        "referenceImage": "参考图片",
        "referenceName": "参考商品名称",
        "firstCategory": "一级分类",
        "secondCategory": "二级分类",
        "thirdCategory": "三级分类",
        "aesPin": "加密的用户标识",
        "days": "评论天数",
        "afterDays": "评论后的天数"
    }

    # 处理每个评论
    for i, comment in enumerate(data['comments']):
        # 添加注释信息
        comment['_comments'] = comments_info
        # 将评论添加到列表中
        all_comments.append(comment)

    # 查找“下一页”按钮
    next_button = dp.ele('css:#comment-0 > div.com-table-footer > div > div > a.ui-pager-next')

    if next_button and not next_button.attr('class').find('disabled') != -1:
        # 点击“下一页”按钮
        next_button.click()
        # 等待页面加载
        time.sleep(2)  # 可能需要根据实际情况调整等待时间
        current_page += 1
    else:
        # 如果没有“下一页”按钮或按钮被禁用，退出循环
        break

# 将所有评论写入同一个文件
with open('all_comments.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=4)

print("所有评论已保存到 all_comments.json 文件中")
