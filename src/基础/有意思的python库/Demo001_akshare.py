from pprint import pprint

import akshare as ak
from datetime import datetime

# 获取加密货币现货数据
# 通过akshare库的crypto_js_spot接口获取加密货币现货行情数据，
# 并使用pprint格式化打印输出结果
crypto_js_spot_df = ak.crypto_js_spot()
pprint(crypto_js_spot_df)

# 获取黄金价格数据
# 获取黄金Au99.99合约的历史数据
gold_data = ak.spot_hist_sge(symbol="Au99.99")
print(gold_data.head())

# 获取所有交易品种
symbols = ak.spot_symbol_table_sge()
pprint(symbols)


# 获取黄金基准价近期数据
golden_benchmark = ak.spot_golden_benchmark_sge()
pprint(golden_benchmark.tail(30))

# 获取白银基准价近期数据
silver_benchmark = ak.spot_silver_benchmark_sge()
pprint(silver_benchmark.tail(30))

# 获取CCTV新闻
# 获取最新日期的最新的CCTV新闻
cctv_news = ak.news_cctv()
pprint(cctv_news)
pprint(cctv_news.tail(30))


# 获取指定股票的个股信息数据
# 参数:
#   symbol: 股票代码，字符串格式，如 "000001"
# 返回值:
#   DataFrame格式的股票个股信息数据

stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001")
pprint(stock_individual_info_em_df)

# 获取指定股票的基本信息数据
# 参数说明:
#   symbol: 股票代码，格式为市场代码+股票编号，如"SH601127"表示上海市场601127股票
# 返回值说明:
#   返回包含股票基本信息的DataFrame数据框，包含股票的各类基础数据字段
stock_individual_basic_info_xq_df = ak.stock_individual_basic_info_xq(symbol="SH601127")

# 打印输出获取到的股票基本信息数据
pprint(stock_individual_basic_info_xq_df)
