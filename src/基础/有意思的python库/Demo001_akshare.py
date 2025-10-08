from pprint import pprint

import akshare as ak

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
print(symbols)


# 获取黄金基准价近期数据
golden_benchmark = ak.spot_golden_benchmark_sge()
print(golden_benchmark.tail(30))

# 获取白银基准价近期数据
silver_benchmark = ak.spot_silver_benchmark_sge()
print(silver_benchmark.tail(30))
