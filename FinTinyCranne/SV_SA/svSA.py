import traceback
import copy
import numpy as np

# 利用模拟退火算法寻找Heston模型最优参数
# 目标函数为：最小化市场价格和Heston模型价格的均方误差

from FinModel.Heston_Model import Heston_Model
import numpy as np
import copy


# 将x增加一个随机变动量，但会把x限制在a,b之内
def random_range(x, a, b):
    random = np.random.normal(0, 0.01 * (b - a), 1)[0]
    if x + random > b:
        random = -np.abs(random)  # 如果新值超越最大值，就将增量变为负数
    elif x + random < a:
        random = np.abs(random)  # 如果新值超越最小值，就将增量变为正数
    return x + random

# 模拟退火算法
class NG:
    def __init__(self, func, x0):
        """
        x0  -列表：函数的初始值
                [v0,kappa,theta,sigma,rho]
        func    -待求解函数
        """
        self.x = x0
        self.dim_x = len(x0)  # 解的维度
        self.func = func
        self.f = func(self.x)  # 计算y值

        self.x_best = self.x  # 记录下来历史最优解，即所有循环中的最优解
        self.f_best = self.f

        self.times_stay = 0  # 连续未接受新解的次数
        self.times_stay_max = 400  # 当连续未接受新解超过这个次数，终止循环

        self.T = 100  # 初始温度：初始温度越高，前期接受新解的概率越大
        self.speed = 0.7  # 退火速度：温度下降速度越快，后期温度越低，接受新解的概率越小，从而最终稳定在某个解附近
        self.T_min = 1e-6  # 最低温度：当低于该温度时，终止全部循环
        self.xf_best_T = {}  # 记录下接受的所有新解

        # 最初若函数值变动为delta，则认为函数值变动很大，可以产生p_expec概率接受新解
        # 若在初期便产生巨大的概率接受新解，则前期寻找新解的过程将变成盲目的随机漫步毫无意义，因此利用alpha调节概率
        self.p_expec = 0.9
        self.delta_standard = 0.7
        self.alpha = self.find_alpha()  # 调节概率因子

        self.times_delta_samller = 0  # 统计新旧最优值之差绝对值连续小于某值的次数
        self.delta_min = (
            0.001  # 当新旧最优值之差绝对值连续小于此值达到某一次数时，终止该温度循环
        )
        self.times_delta_min = (
            100  # 当新旧最优值之差绝对值连续小于此值达到这个次数时，终止该温度循环
        )

        self.times_max = 500  # 当每个温度下循环超过这个次数，终止该温度循环
        self.times_cycle = 0  # 记录算法循环总次数

        self.times_p = 0  # 统计因为p值较大而接受新解的次数

        self.xf_all = {
            self.times_cycle: [self.x, self.f]
        }  # 记录下来每一次循环产生的新解和函数值
        self.xf_best_all = {
            self.times_cycle: [self.x, self.f]
        }  # 记录下来每一次循环接受的新解和函数值

    # 温度下降，产生新温度
    def T_change(self):
        self.T = self.T * self.speed
        print(
            "当前温度为{},大于最小温度{}".format(self.T, self.T_min)
        )  # 展示当前温度和最小温度

    # 将所有的x和f、循环次数存储下来
    def save_xy(self):
        self.xf_all[self.times_cycle] = [self.x, self.f]

    # 将所有的最优x,y、循环次数存储下来
    def save_best_xy(self):
        self.xf_best_all[self.times_cycle] = [self.x, self.f]

    # 当调节因子为alpha时，函数值变动值为delta产生的接受新解概率
    def __p_delta(self, alpha):
        return np.exp(-self.delta_standard / (self.T * alpha))

    # 用二分法寻找方程解
    def __find_solver(self, func, f0):
        """
        输入：
        func    -待求解方程的函数
        f0  -float,预期函数值
        输出：
        mid -float,函数=预期函数值 的解
        """
        up = 100
        down = 0.00001
        mid = (up + down) / 2
        while abs(func(mid) - f0) > 0.0001:
            if func(down) < f0 < func(mid):
                up = mid
                mid = (mid + down) / 2
            elif func(up) > f0 > func(mid):
                down = mid
                mid = (up + down) / 2
            else:
                print("error!")
                break
        return mid

    # 最初若函数值变动为delta，则认为函数值变动很大，可以产生p_expec概率接受新解
    def find_alpha(self):
        return self.__find_solver(self.__p_delta, self.p_expec)

    # 获得新的x
    def get_x_new(self):
        random = np.random.normal(0, 1, self.dim_x)  # 新的随机增量
        return self.x + random

    # 判断是否可以接受新的解
    def judge(self):
        if self.delta < 0:  # 如果函数值变动幅度小于0,则接受新解
            self.x = self.x_new
            self.f_last = self.f  # 在最优解函数值更新之前将其记录下来
            self.f = self.f_new
            self.save_best_xy()  # 记录每次循环接受的新解
            self.get_history_best_xy()  # 更新历史最优解
            self.times_stay = 0  # 由于未接受新解，将连续未接受新解的次数归零
            print(
                "由于函数值变小新接受解{}:{}".format(self.f, self.x)
            )  # 展示当前接受的新解
        else:
            p = np.exp(-self.delta / (self.T * self.alpha))  # 接受新解的概率
            p_ = np.random.random()  # 判断标准概率
            if p > p_:  # 如果概率足够大，接受新解
                self.x = self.x_new
                self.f_last = self.f  # 在接受的新解更新之前将其记录下来
                self.f = self.f_new
                self.save_best_xy()  # 记录每次循环接受的新解
                self.get_history_best_xy()  # 更新历史最优解
                print(
                    "由于概率{}大于{}，新接受解{}:{}".format(p, p_, self.f, self.x)
                )  # 展示当前接受的新解
                self.times_p += 1  # 统计因为概率而接受新解的次数
                self.times_stay = 0  # 由于未接受新解，将连续未接受新解的次数归零
            else:
                if self.time_ == 0:
                    self.f_last = self.f  # 在接受的新解更新之前将其记录下来
                self.times_stay += 1  # 连续接受新解次数加1
                print("连续未接受新解{}次".format(self.times_stay))

    # 获得历史最优解
    def get_history_best_xy(self):
        x_array = list(
            np.array(list(self.xf_best_all.values()),dtype=object)[:, 0]
        )  # 从历史所有的最优x和f中获得所有的x
        f_array = list(
            np.array(list(self.xf_best_all.values()),dtype=object)[:, 1]
        )  # 从历史所有的最优x和f中获得所有的f
        self.f_best = min(f_array)  # 从每阶段最优的f中获得最优的f
        self.x_best = x_array[f_array.index(self.f_best)]  # 利用最优f反推最优x
        return self.x_best, self.f_best


    # 统计新旧函数值之差的绝对值连续小于此值的次数
    def count_times_delta_smaller(self):
        if self.delta_best < self.delta_min:
            self.times_delta_samller += (
                1  # 如果新旧函数值之差绝对值小于某值，则次数加1，否则归零
            )
        else:
            self.times_delta_samller = 0
        print(
            "差值{}连续小于{}达到{}次".format(
                self.delta_best, self.delta_min, self.times_delta_samller
            )
        )

    # 终止循环条件
    def condition_end(self):
        if (
            self.times_delta_samller > self.times_delta_min
        ):  # 如果新旧函数值之差绝对值连续小于某值次数超过某值，终止该温度循环
            return True
        elif (
            self.times_stay > self.times_stay_max
        ):  # 当连续未接受新解超过这个次数，终止循环
            return True

    # 在某一特定温度下进行循环
    def run_T(self):

        for time_ in range(self.times_max):
            self.time_ = time_
            self.x_new = self.get_x_new()  # 获得新解
            self.f_new = self.func(self.x_new)  # 获得新的函数值
            self.save_xy()  # 将新解和函数值记录下来
            self.delta = self.f_new - self.f  # 计算函数值的变化值
            self.judge()  # 判断是否接受新解
            self.times_cycle += 1  # 统计循环次数
            self.delta_best = np.abs(
                self.f - self.f_last
            )  # 上次函数值与这次函数值的差值绝对值
            self.count_times_delta_smaller()  # 统计新旧函数值之差的绝对值连续小于此值的次数
            if self.condition_end() == True:  # 如果满足终止条件，终止该温度循环
                print(
                    "满足终止条件：接受新解后的函数值变化连续小于{}达到次数".format(
                        self.delta_min
                    )
                )
                break
            print(
                "当前历史最优解{}：{}".format(self.f_best, self.x_best)
            )  # 展示当前最优值
            print("当前接受的新解{}：{}".format(self.f, self.x))  # 展示当前接受的新解
            print("当前新解{}：{}".format(self.f_new, self.x_new))  # 展示当前新产生的解
            print("当前温度为{}".format(self.T))  # 展示当前温度

    # 当每个温度下的循环结束时，有一定概率将当前接受的新解替换为历史最优解
    def accept_best_xf(self):
        if np.random.random() > 0.75:
            self.x = self.x_best
            self.f = self.f_best

    def run(self):
        while self.T > self.T_min:
            self.run_T()  # 循环在该温度下的求解
            self.xf_best_T[self.T] = [
                self.get_history_best_xy()
            ]  # 记录在每一个温度下的最优解
            self.T_change()  # 温度继续下降
            self.accept_best_xf()  # 当每个温度下的循环结束时，有一定概率将当前接受的新解替换为历史最优解
            if self.condition_end() == True:  # 如果满足终止条件，终止该温度循环
                break



class NGHeston(NG):
    def __init__(self, func, x0):
        super().__init__(func, x0)
        self.T = 90#初始温度
        self.T_min = 1e-7  # 由于算法耗时太长，故小做一段模拟试试看
        self.times_max = 500#每个温度下循环次数

    # sv模型的各个参数由于存在取值范围，因此在获得新的参数估计值时需要对其取值范围加以限制
    def get_x_new(self):
        """
        [v0,kappa,theta,sigma,rho]
        其中：
        v0,kappa,theta,sigma>0
        -1<rho<1
        2kappa*theta>sigma**2
        """
        x = copy.deepcopy(self.x)  # 使用深copy，否则self.x会随着x一起变动
        x[0] = random_range(x[0], 0, 5)
        x[1] = random_range(x[1], 0, 1)
        x[2] = random_range(x[2], 0, 1)
        x[3] = random_range(x[3], 0, 3)
        x[4] = random_range(x[4], -1, 1)
        return x



class SV_SA:

    def __init__(
        self,
        data,
        v0: float = 0.01,
        kappa: float = 2,
        theta: float = 0.1,
        sigma: float = 0.1,
        rho: float = -0.5,
    ):
        """输入数据

        data    -pandas.core.frame.DataFrame格式数据，具体样式如下：

                           K         t        s0         r       c
                30     2.150  0.194444  2.111919  0.031060  0.0546
                31     2.150  0.198413  2.115158  0.031120  0.0666
                32     2.150  0.202381  2.107673  0.031210  0.0627
                33     2.150  0.214286  2.122269  0.031250  0.0531
                90     3.240  0.202381  3.181339  0.047446  0.0724

        """

        self.data = data
        self.init_params = [v0, kappa, theta, sigma, rho]  # 初始参数列表
        self.cycle = 0  # 计算模拟退火算法轮数
        self.error = 0.000000


    def error_mean_percent(self, init_params: list):
        """计算heston模型期权定价的百分比误差均值

        百分比误差均值=绝对值（（理论值-实际值）/实际值）/样本个数

        输入：
        init_params -初始参数,列表格式
                     [v0,kappa,theta,sigma,rho]

        返回： -误差百分点数   例如：返回5，表示5%
        """
        v0, kappa, theta, sigma, rho = init_params
        list_p_sv = []
        for i in self.data.index:
            K, t, s0, r, p_real = self.data.loc[i, :].tolist()
            sv = Heston_Model(
                K=K,
                t=t,
                S0=s0,
                r=r,
                v0=v0,
                kappa=kappa,
                theta=theta,
                sigma=sigma,
                rho=rho,
            )
            p_sv = sv.Call_Value()  # sv模型期权价格
            list_p_sv.append(p_sv)

        self.error = np.average(
            np.abs((np.array(list_p_sv) - self.data["c"]) / self.data["c"])
        )  # sv模型的期权价格和实际价格的百分比误差均值
        print("\n")
        print("第{}轮,误差：{}".format(self.cycle, self.error))  # 展示本轮的误差
        self.cycle += 1

        return self.error


if __name__ == "__main__":
    print("#调用函数")#调用函数