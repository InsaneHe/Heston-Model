"""
此文件通过BSM模型计算期权的理论价值
"""
def option_BSM(S, K, sigma, r, T, opt):
    """
    定义一个运用布莱克-斯科尔斯-默顿模型计算欧式期权价格的函数
    S：代表期权基础资产的价格
    K：代表期权的行权价格
    sigma：代表基础资产收益率的波动率
    r：代表连续复利的无风险收益率
    T：代表期权的期限（年）
    opt：代表期权类型，输入opt="call"表示看涨期权，输入其他则表示看跌期权
    """
    from numpy import log, exp, sqrt  # 从NumPy模块导入log、exp、sqrt这3个函数
    from scipy.stats import norm  # 从SciPy的子模块stats导入norm函数
    d1 = (log(S / K) + (r + pow(sigma, 2) / 2) * T) / (sigma * sqrt(T))  # 计算参数d1
    d2 = d1 - sigma * sqrt(T)  # 计算参数d2
    if opt == "call":  # 针对欧式看涨期权
        value = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)  # 计算期权价格
    else:  # 针对欧式看跌期权
        value = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)  # 计算期权价格
    return value
    pass
