from DrissionPage import ChromiumPage

# 实例化浏览器对象
dp = ChromiumPage()
dp.listen.start('api.m.jd.com')
# 设置访问地址
Url = "https://item.jd.com/100076766489.html"
dp.get(Url)
dp.ele('').click()
json_data = dp.listen.wait().response.body
print(json_data)
