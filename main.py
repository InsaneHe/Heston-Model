# main.py
from Heston_Model import calculate_heston_option_value
from BSM_Model import option_BSM
from Backtrader_Strategy import run_strategy
from Visualization import plot_results

def main():
    # 假设这里我们已经有了期权的参数和市场数据
    expiration_date = ql.Date(9, 11, 2022)  # 期权到期日
    strikes = [...]  # 执行价格列表
    spot_price = 659.37  # 现货价格
    # ... 其他参数

    # 计算BSM模型和Heston模型的理论价值
    bsm_values = option_BSM(expiration_date, strikes, spot_price)
    heston_values = calculate_heston_option_value(expiration_date, strikes, spot_price)

    # 运行backtrader策略
    strategy_results = run_strategy(spot_price)

    # 可视化结果
    plot_results(bsm_values, heston_values, strategy_results)

if __name__ == "__main__":
    main()
