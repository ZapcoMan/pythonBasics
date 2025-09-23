import pandas as pd
import numpy as np

def clean_crocodile_data():
    """
    清洗鳄鱼数据集
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
    
    # 2. 处理价格列，去除逗号并转换为数值
    df['price_usd'] = df['price_usd'].astype(str).str.replace(',', '').astype(float)
    
    # 3. 处理24小时交易量列，去除$和字母并转换为数值
    def convert_volume(vol_str):
        if pd.isna(vol_str):
            return np.nan
        vol_str = str(vol_str).replace('$', '').replace('K', '000').replace('M', '000000').replace('B', '000000000')
        # 处理类似 "1.86B" 的格式
        if '000' in vol_str:
            number_part = vol_str.split('000')[0]
            zeros_part = vol_str.split('000')[1]
            if zeros_part == '':
                return float(number_part) * 1000
            else:
                return float(number_part + zeros_part)
        else:
            return float(vol_str)
    
    df['vol_24h'] = df['vol_24h'].apply(convert_volume)
    df['total_vol'] = df['total_vol'].str.rstrip('%').astype(float)
    df['chg_24h'] = df['chg_24h'].str.rstrip('%').astype(float)
    df['chg_7d'] = df['chg_7d'].str.rstrip('%').astype(float)
    
    # 4. 处理市值列
    def convert_market_cap(mc_str):
        if pd.isna(mc_str):
            return np.nan
        mc_str = str(mc_str).replace('$', '').replace('K', '000').replace('M', '000000').replace('B', '000000000').replace('T', '000000000000')
        # 处理类似 "40.45B" 或 "2.31T" 的格式
        if '000' in mc_str:
            number_part = mc_str.split('000')[0]
            zeros_part = mc_str.split('000')[1]
            if zeros_part == '':
                return float(number_part) * 1000
            else:
                return float(number_part + zeros_part)
        else:
            return float(mc_str)
    
    df['market_cap'] = df['market_cap'].apply(convert_market_cap)
    
    # 5. 转换时间戳列为datetime类型
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print("\n清洗后数据形状:", df.shape)
    
    # 保存清洗后的数据
    df.to_csv('cryptocurrency_cleaned.csv', index=False)
    print("\n加密货币数据清洗完成，已保存到 cryptocurrency_cleaned.csv")
    
    return df

def main():
    """
    主函数，执行数据清洗
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