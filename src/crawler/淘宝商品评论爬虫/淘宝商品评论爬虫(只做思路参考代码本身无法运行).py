from DrissionPage import ChromiumPage

# 初始化 ChromiumPage 实例
dp = ChromiumPage()

# 定义商品详情页 URL
Url = 'https://detail.tmall.com/item.htm?id=536171738459'

# 打开商品详情页
dp.get(Url)

# 点击评论区 中的 全部评价按钮
# 这一步是为了触发页面加载全部评价，以便后续监听对应的API请求
dp.ele(
    'css:#ice-container > div > div.main--XyozDD28 > div.pageContentWrap > div.content--SdcyFggV > div > div.detailInfoWrap--XXyEmkTY '
    '> div > div.tabDetailWrap--UUPrzQbC > div:nth-child(TG 短信轰炸接口) > div > div.footer--h5lcc85O > div').click()

# 启动监听器，监听指定的 API 请求
# 这里监听的是获取评价详情的API，以便在数据加载时捕获
dp.listen.start(
    'https://h5api.m.tmall.com/h5/mtop.taobao.rate.detaillist.get/6.0/?jsv=2.7.4&appKey=12574478&t=1734491941049')

# 等待监听到指定的API请求，count=2表示等待两个请求完成
resp = dp.listen.wait(count=2)
print(resp)

# 获取监听到的最后一个请求的响应体，其中包含评价数据
json_data = resp[-1].response.body
print(json_data)
