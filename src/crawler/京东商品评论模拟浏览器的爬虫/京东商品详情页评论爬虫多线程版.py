import json
from DrissionPage import ChromiumPage
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# 实例化浏览器对象
def fetch_comments(page_number):
    dp = ChromiumPage()

    # 设置访问地址
    Url = "https://item.jd.com/100076766489.html"

    # 监听数据包
    dp.listen.start('https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments')

    # 访问商品页面
    dp.get(Url)

    # 点击查看评论
    dp.ele('css:#detail > div.tab-main.large > ul > li:nth-child(5)').click()

    # 初始化评论列表
    all_comments = []

    # 跳转到指定页数
    if page_number > 1:
        for _ in range(page_number - 1):
            next_button = dp.ele('css:#comment-0 > div.com-table-footer > div > div > a.ui-pager-next')
            if next_button and not next_button.attr('class').find('disabled') != -1:
                next_button.click()
                time.sleep(2)  # 可能需要根据实际情况调整等待时间
            else:
                break

    # 等待数据包加载
    resp = dp.listen.wait()

    # 获取响应数据
    json_data = resp.response.body

    # 解析JSON数据
    if isinstance(json_data, str):
        data = json.loads(json_data)
    elif isinstance(json_data, dict):
        data = json_data
    else:
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
        comment['_comments'] = comments_info
        all_comments.append(comment)

    dp.close()
    return all_comments


# 最大页数限制，防止无限循环
max_pages = 20

# 使用多线程加速爬虫
all_comments = []
with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_page = {executor.submit(fetch_comments, page): page for page in range(1, max_pages + 1)}
    for future in as_completed(future_to_page):
        page = future_to_page[future]
        try:
            comments = future.result()
            all_comments.extend(comments)
            print(f"完成第 {page} 页的评论抓取")
        except Exception as e:
            print(f"第 {page} 页的评论抓取失败: {e}")

# 将所有评论写入同一个文件
with open('京东评论区.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=4)

print("所有评论已保存到 京东评论区.json 文件中")
