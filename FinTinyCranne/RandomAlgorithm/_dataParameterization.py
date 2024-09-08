import traceback
import pandas as pd
import numpy as np
from typing import Union, Tuple, Any
from SV_SA.svSA import SV_SA, NGHeston
from OrgDefinedValue._userConstant import *

def GetBestPara(date_start_str: str = "20200612", date_end_str: str = "20200912"):
    data=pd.read_csv(UserConstant.READ_CSV_SHANG_ZHENG_50_ETF_OPTION_RELATIVE_PATH) #读取原始数据
    #data=pd.read_csv(UserConstant.READ_CSV_SHANG_ZHENG_50_ETF_OPTION_FULL_PATH) #读取原始数据

    date_start_train = 20200612                          #指定待训练数据的开始日期为2020年6月12日
    date_end_train = 20200912                            #指定待训练数据的结束日期为2020年9月12日

    option = data[
        (data["交易日期"] >= date_start_train) & (data["交易日期"] <= date_end_train)
    ]  # 选择指定日期的数据

    option=option[option['看涨看跌类型']=='C']            #训责看涨期权类型
    option=option[['执行价格','剩余到期时间（年）','上证50ETF价格','无风险收益率（shibor)','期权收盘价']]
    option.columns=['K','t','s0','r','c']               #将数据列标题修改为指定列标题

    ###############################################model=SV_SA(data=option)#建立类
    ###############################################model.sa()#开始训练模型，不停地寻找最优解
    ###############################################model.ng.get_history_best_xy()#查看最优解，即能使总误差最小的heston模型的五个参数

    return GetOptimizedSolutionValue(dataOption = option)

def GetOptimizedSolutionValue(dataOption: Union):


        model=SV_SA(data=dataOption)#建立类
        ##model.sa()#开始训练模型，不停地寻找最优解
        OptimazationByModelTrainingAndGetHistoryBestXy(model)


        ##model.ng.get_history_best_xy()#查看最优解，即能使总误差最小的heston模型的五个参数

def OptimazationByModelTrainingAndGetHistoryBestXy(model: SV_SA, **kwargs) -> Tuple[Any, Any]:
    """对均方误差函数用模拟退火算法计算最优值"""
    self_ng = NGHeston(func=model.error_mean_percent, x0=model.init_params)
    self_ng.run()
    self_x_star, self_y_star = self_ng.get_history_best_xy()
    print(self_x_star, self_y_star)  # 生成最优解x和最优值y

    x_array = list(
            np.array(list(model.xf_best_all.values()),dtype=object)[:, 0]
        )  # 从历史所有的最优x和f中获得所有的x
    f_array = list(
            np.array(list(model.xf_best_all.values()),dtype=object)[:, 1]
        )  # 从历史所有的最优x和f中获得所有的f
    f_best = min(f_array)  # 从每阶段最优的f中获得最优的f
    x_best = x_array[f_array.index(f_best)]  # 利用最优f反推最优x
    return x_best, f_best


if __name__ == "__main__":
    GetBestPara()#调用函数