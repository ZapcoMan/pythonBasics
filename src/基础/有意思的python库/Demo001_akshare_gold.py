import akshare as ak
# 获取黄金Au99.99合约的历史数据
gold_data = ak.spot_hist_sge(symbol="Au99.99")
# print(gold_data.tail(30))
# 查看数据中的最新日期
# print(gold_data['date'].max())
gold_spot = ak.spot_gold()
print(gold_spot)

# 可以尝试获取实时行情数据
# 实时行情数据
print("实时行情:")
print(gold_spot)

# 历史数据最新日期
print("历史数据最新日期:")
print(gold_data['date'].max())
