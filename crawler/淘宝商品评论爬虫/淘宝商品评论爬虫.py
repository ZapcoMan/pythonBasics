from DrissionPage import ChromiumPage

# 初始化 ChromiumPage 实例
dp = ChromiumPage()

# 定义商品详情页 URL
Url = 'https://detail.tmall.com/item.htm?id=536171738459'

# 启动监听器，监听指定的 API 请求
dp.listen.start('https://h5api.m.tmall.com/h5/mtop.taobao.rate.detaillist.get/6.0/?jsv=2.7.4&appKey=12574478&t=1734488487104')

# 打开商品详情页
dp.get(Url)

# 通过 CSS 选择器定位并获取页面中的某个元素
element = dp.ele('css:#ice-container > div > div.main--XyozDD28 > div.pageContentWrap > div.content--SdcyFggV > div > div.detailInfoWrap--XXyEmkTY '
                 '> div > div.tabDetailWrap--UUPrzQbC > div:nth-child(1) > div > div.footer--h5lcc85O > div').click()


comments = element.text

# 打印评论内容
print(comments)


