import yfinance as yf

# 下载单只股票的历史数据（以“惠丰钻石”为例，股票代码为 839725）
stock_code = '839725.SS'  # 股票代码格式（如深市用 .SZ，沪市用 .SS）
stock_data = yf.download(stock_code, start="2023-01-01", end="2024-12-31")

# 显示获取的数据
print(stock_data.head())

# 保存数据为 CSV 文件
stock_data.to_csv('惠丰钻石_data.csv')
