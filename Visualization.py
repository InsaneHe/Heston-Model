# Visualization.py
import matplotlib.pyplot as plt

def plot_results(bsm_values, heston_values, strategy_results):
    # 绘制BSM模型、Heston模型和策略结果的比较图
    plt.figure()
    plt.plot(bsm_values, label = "BSM Model")
    plt.plot(heston_values, label = "Heston Model")
    plt.plot(strategy_results, label = "Strategy Results")
    plt.legend()
    plt.show()
