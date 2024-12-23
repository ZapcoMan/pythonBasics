import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.impute import SimpleImputer

# 1. 数据加载
# 假设您的股市数据保存在 'data.csv' 文件中
data = pd.read_csv('data.csv')

# 2. 数据预处理
# 去掉 '代码' 和 '名称' 列
data = data.drop(columns=['代码', '名称'])


# 定义单位转换函数
def convert_units(value):
    """
    将含有单位的字符串转换为浮点数。
    如果值是 '--' 或 '亏损'，返回 np.nan。
    如果值是数字类型，直接返回。
    """
    if isinstance(value, str):
        # 将‘亿’和‘万’转换为科学计数法
        value = value.replace('亿', 'e8').replace('万', 'e4')

        # 如果值是 '--' 或 '亏损'，直接返回 np.nan
        if value in ['--', '亏损']:
            return np.nan

        try:
            # 尝试将字符串转换为浮点数
            value = float(value)
        except ValueError:
            # 如果转换失败，处理异常情况
            print(f"无法转换: {value}")
            return np.nan  # 返回缺失值
    elif isinstance(value, (int, float)):
        return value
    else:
        print(f"未知类型: {type(value)}")
        return np.nan

    return value


# 替换所有 '--' 和 '亏损' 为 np.nan
data.replace(['--', '亏损'], np.nan, inplace=True)

# 处理“成交额”、“流通股”和“流通市值”列的单位转换
for col in ['成交额', '流通股', '流通市值']:
    data[col] = data[col].apply(convert_units)

# 检查是否有缺失值
print("处理后的数据中缺失值的数量:")
print(data.isnull().sum())

# 3. 填充缺失值
# 分别处理数值列和非数值列
numeric_cols = data.select_dtypes(include=[np.number]).columns
non_numeric_cols = data.select_dtypes(exclude=[np.number]).columns

# 对数值列使用均值填充
imputer_numeric = SimpleImputer(strategy='mean')
data[numeric_cols] = imputer_numeric.fit_transform(data[numeric_cols])

# 对非数值列使用常量填充（例如：-999）
imputer_non_numeric = SimpleImputer(strategy='constant', fill_value=-999)
data[non_numeric_cols] = imputer_non_numeric.fit_transform(data[non_numeric_cols])

# 4. 数据标准化
scaler = StandardScaler()
data_scaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)

# 5. 特征选择与目标变量选择
X = data_scaled[
    ['现价', '涨跌幅(%)', '涨跌', '涨速(%)', '换手(%)', '量比', '振幅(%)', '成交额', '流通股', '流通市值', '市盈率']]
y = data_scaled['现价']  # 目标变量是 '现价'

# 6. 数据划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 7. 模型训练与预测
svm_model = SVR(kernel='rbf')  # 使用支持向量机回归模型
svm_model.fit(X_train, y_train)

# 对测试集进行预测
y_pred_svm = svm_model.predict(X_test)

# 8. 模型评估
mae_svm = mean_absolute_error(y_test, y_pred_svm)
r2_svm = r2_score(y_test, y_pred_svm)

# 输出评估结果
print(f"SVM MAE: {mae_svm:.4f}")
print(f"SVM R²: {r2_svm:.4f}")

# 打印预测值与真实值的对比
comparison = pd.DataFrame({'真实值': y_test, '预测值': y_pred_svm})
print("部分预测结果与真实值对比：")
print(comparison.head())
