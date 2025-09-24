import pandas as pd
import numpy as np

def clean_crocodile_data():
    """
    清洗鳄鱼数据集

    该函数读取鳄鱼数据集文件，执行数据清洗操作，包括：
    1. 删除重复行
    2. 过滤异常值（长度和重量）
    3. 标准化性别列
    4. 保存清洗后的数据到新文件

    Returns:
        pandas.DataFrame: 清洗后的鳄鱼数据
    """
    # 读取数据
    df = pd.read_csv('crocodile_dataset.csv')

    print("原始数据形状:", df.shape)
    print("原始数据列:", df.columns.tolist())

    # 查看前几行数据
    print("\n前5行数据:")
    print(df.head())

    # 检查缺失值
    print("\n缺失值统计:")
    print(df.isnull().sum())

    # 检查重复值
    print("\n重复行数:", df.duplicated().sum())

    # 数据类型检查
    print("\n数据类型:")
    print(df.dtypes)

    # 清洗工作
    # 1. 删除完全重复的行
    df = df.drop_duplicates()

    # 2. 处理数值列中的异常值
    # 检查长度和重量是否合理
    df = df[(df['Observed Length (m)'] > 0) & (df['Observed Length (m)'] < 10)]
    df = df[(df['Observed Weight (kg)'] >= 0) & (df['Observed Weight (kg)'] < 2000)]

    # 3. 标准化性别列
    # 将Sex列中的'Unknown'替换为NaN
    df['Sex'] = df['Sex'].replace('Unknown', np.nan)

    # 4. 标准化年龄列
    # 将Age Class列中的值标准化
    age_mapping = {
        'Hatchling': 'Hatchling',
        'Juvenile': 'Juvenile',
        'Subadult': 'Subadult',
        'Adult': 'Adult'
    }
    # 已经是标准格式，不需要映射

    print("\n清洗后数据形状:", df.shape)

    # 保存清洗后的数据
    df.to_csv('crocodile_dataset_cleaned.csv', index=False)
    print("\n鳄鱼数据清洗完成，已保存到 crocodile_dataset_cleaned.csv")

    return df

def clean_cryptocurrency_data():
    """
    清洗加密货币数据集

    该函数读取加密货币数据集文件，执行数据清洗操作，包括：
    1. 删除重复行
    2. 转换价格、交易量、市值等列的数据格式
    3. 处理百分比数据和带单位的数值
    4. 转换时间戳格式
    5. 保存清洗后的数据到新文件

    Returns:
        pandas.DataFrame: 清洗后的加密货币数据
    """
    # 读取数据
    df = pd.read_csv('cryptocurrency.csv')

    print("\n\n加密货币数据清洗")
    print("原始数据形状:", df.shape)
    print("原始数据列:", df.columns.tolist())

    # 查看前几行数据
    print("\n前5行数据:")
    print(df.head())

    # 检查缺失值
    print("\n缺失值统计:")
    print(df.isnull().sum())

    # 检查重复值
    print("\n重复行数:", df.duplicated().sum())

    # 数据类型检查
    print("\n数据类型:")
    print(df.dtypes)

    # 清洗工作
    # 1. 删除完全重复的行
    df = df.drop_duplicates()

    # 2. 处理价格列，去除符号和单位并转换为数值
    def convert_price(price_str):
        """
        转换价格字符串为浮点数

        支持处理带有货币符号($), 千位分隔符(,), 百分比(%)以及单位(K, M, B, T)的价格字符串

        Args:
            price_str: 价格字符串

        Returns:
            float or numpy.nan: 转换后的数值，如果输入为空则返回numpy.nan
        """
        if pd.isna(price_str):
            return np.nan
        price_str = str(price_str).replace('$', '').replace(',', '')
        if '%' in price_str:
            return float(price_str.replace('%', '')) / 100
        if 'T' in price_str:
            return float(price_str.replace('T', '')) * 1e12
        elif 'B' in price_str:
            return float(price_str.replace('B', '')) * 1e9
        elif 'M' in price_str:
            return float(price_str.replace('M', '')) * 1e6
        elif 'K' in price_str:
            return float(price_str.replace('K', '')) * 1e3
        else:
            return float(price_str)

    df['price_usd'] = df['price_usd'].apply(convert_price)

    # 3. 处理24小时交易量列
    def convert_volume(vol_str):
        """
        转换交易量字符串为浮点数

        支持处理带有货币符号($), 千位分隔符(,), 百分比(%)以及单位(K, M, B, T)的交易量字符串

        Args:
            vol_str: 交易量字符串

        Returns:
            float or numpy.nan: 转换后的数值，如果输入为空则返回numpy.nan
        """
        if pd.isna(vol_str):
            return np.nan
        vol_str = str(vol_str).replace('$', '').replace(',', '')
        if '%' in vol_str:
            return float(vol_str.replace('%', '')) / 100
        if 'T' in vol_str:
            return float(vol_str.replace('T', '')) * 1e12
        elif 'B' in vol_str:
            return float(vol_str.replace('B', '')) * 1e9
        elif 'M' in vol_str:
            return float(vol_str.replace('M', '')) * 1e6
        elif 'K' in vol_str:
            return float(vol_str.replace('K', '')) * 1e3
        else:
            return float(vol_str)

    df['vol_24h'] = df['vol_24h'].apply(convert_volume)

    # 4. 处理总交易量列
    df['total_vol'] = df['total_vol'].apply(convert_volume)

    # 5. 处理百分比列和带有单位的数值列
    df['chg_24h'] = df['chg_24h'].apply(convert_volume)
    df['chg_7d'] = df['chg_7d'].apply(convert_volume)

    # 6. 处理市值列
    df['market_cap'] = df['market_cap'].apply(convert_volume)

    # 7. 转换时间戳列为datetime类型
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print("\n清洗后数据形状:", df.shape)

    # 保存清洗后的数据
    df.to_csv('cryptocurrency_cleaned.csv', index=False)
    print("\n加密货币数据清洗完成，已保存到 cryptocurrency_cleaned.csv")

    return df

def main():
    """
    主函数，执行数据清洗

    依次调用鳄鱼数据和加密货币数据的清洗函数，完成所有数据清洗工作
    并输出清洗结果的统计信息
    """
    print("开始数据清洗...")

    # 清洗鳄鱼数据
    crocodile_df = clean_crocodile_data()

    # 清洗加密货币数据
    crypto_df = clean_cryptocurrency_data()

    print("\n\n所有数据清洗完成！")
    print("鳄鱼数据集包含 {} 行，{} 列".format(crocodile_df.shape[0], crocodile_df.shape[1]))
    print("加密货币数据集包含 {} 行，{} 列".format(crypto_df.shape[0], crypto_df.shape[1]))

if __name__ == "__main__":
    main()
