"""
此文件通过Heston模型计算期权的理论价值
"""
# Heston_Model.py
import QuantLib as ql
import numpy as np


def calibrate_heston_model(market_prices, strikes, maturities, risk_free_rate, dividend_yield,
                           initial_guess=(0.01, 0.2, 0.02, 0.5, -0.75)):
    """
    校准Heston模型参数

    参数:
    - market_prices: 期权市场价格列表。
    - strikes: 期权行权价格列表。
    - maturities: 期权期限列表，以年为单位。
    - risk_free_rate: 无风险利率。
    - dividend_yield: 股息收益率。
    - initial_guess: Heston模型参数的初始猜测值，元组形式 (v0, kappa, theta, sigma, rho)。

    返回:
    - calibrated_params: 校准后的Heston模型参数。
    """
    # 创建Heston模型参数的估计器
    heston_helpers = []
    for i, maturity in enumerate(maturities):
        maturity_date = ql.Date(int((ql.Date.todaysDate() + ql.Period(maturity, ql.Years)).serialNumber()))
        sigma = np.std([market_prices[i] / strikes[i] for i in range(len(strikes))])  # 初始波动率估计
        helper = ql.HestonModelHelper(ql.Period(maturity, ql.Years),
                                      ql.UnitedStates(),
                                      ql.QuoteHandle(ql.SimpleQuote(market_prices[0] / strikes[0])),
                                      strikes[0],
                                      ql.QuoteHandle(ql.SimpleQuote(sigma)),
                                      ql.YieldTermStructureHandle(
                                          ql.FlatForward(ql.Settings.instance().evaluationDate, risk_free_rate,
                                                         ql.Actual365Fixed())),
                                      ql.YieldTermStructureHandle(
                                          ql.FlatForward(ql.Settings.instance().evaluationDate, dividend_yield,
                                                         ql.Actual365Fixed())))
        heston_helpers.append(helper)

    # 设置优化器和结束标准
    lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
    end_criteria = ql.EndCriteria(ql.MaxIterations(100), ql.WithinTolerance(1e-8), ql.WithinTolerance(1e-8),
                                  ql.WithinTolerance(1e-8))

    # 创建Heston模型并进行参数校准
    process = ql.HestonProcess(ql.YieldTermStructureHandle(
        ql.FlatForward(ql.Settings.instance().evaluationDate, risk_free_rate, ql.Actual365Fixed())),
                               ql.YieldTermStructureHandle(
                                   ql.FlatForward(ql.Settings.instance().evaluationDate, dividend_yield,
                                                  ql.Actual365Fixed())),
                               ql.QuoteHandle(ql.SimpleQuote(market_prices[0] / strikes[0])),
                               *initial_guess)
    model = ql.HestonModel(process)
    model.calibrate(heston_helpers, lm, end_criteria)

    # 返回校准后的参数
    calibrated_params = model.params()
    return calibrated_params


def calculate_heston_option_value(market_prices, strikes, maturities, spot_price, risk_free_rate, dividend_yield):
    """
    使用Heston模型计算期权的理论价值，并进行参数校准。

    参数:
    - market_prices: 期权市场价格列表。
    - strikes: 期权行权价格列表。
    - maturities: 期权期限列表，以年为单位。
    - spot_price: 标的资产的现价。
    - risk_free_rate: 无风险利率。
    - dividend_yield: 股息收益率。

    返回:
    - theoretical_values: Heston模型计算的期权价值列表。
    """
    # 校准Heston模型参数
    calibrated_params = calibrate_heston_model(market_prices, strikes, maturities, risk_free_rate, dividend_yield)

    # 使用校准后的参数设置Heston过程和模型
    process = ql.HestonProcess(
        ql.YieldTermStructureHandle(
            ql.FlatForward(ql.Settings.instance().evaluationDate, risk_free_rate, ql.Actual365Fixed())),
        ql.YieldTermStructureHandle(
            ql.FlatForward(ql.Settings.instance().evaluationDate, dividend_yield, ql.Actual365Fixed())),
        ql.QuoteHandle(ql.SimpleQuote(spot_price)),
        *calibrated_params
    )
    model = ql.HestonModel(process)

    # 创建并定价期权
    theoretical_values = []
    for i in range(len(maturities)):
        maturity_date = ql.Date(
            int((ql.Date.todaysDate() + ql.Period(int(maturities[i] * 365), ql.Days)).serialNumber()))
        payoff = ql.PlainVanillaPayoff(ql.Option.Call, strikes[i])
        exercise = ql.EuropeanExercise(maturity_date)
        option = ql.VanillaOption(payoff, exercise)
        engine = ql.AnalyticHestonEngine(model)
        option.setPricingEngine(engine)
        theoretical_values.append(option.NPV())

    return theoretical_values
    pass
