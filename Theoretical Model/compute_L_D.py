import math

# 海平面最大静推力，标压，TO/GA位
F0 = 11932.4 * 2  # KG
Fclimb = 2487.8 * 2
Fcruise = 2218 * 2
"""
本程序可能需要调的地方：
1）取不同阶段的所需推力，起飞过程中将20000英尺以下定为爬升；
下降过程将10000英尺以下定为下降，其余按照平飞计算
"""

# 计算阻力系数，依据马赫数、升力系数
def computer_Cd_polarcurve(M, Cl):

    if M < 0.29:
        # 计算升力系数，此处为低速极曲线计算
        Cd = 0.02062 * math.pow(Cl, 3) + 0.01561 * math.pow(Cl, 2) + 0.007846 * Cl + 0.01868
    elif M <= 0.3:
        Cd = 0.1266 * math.pow(Cl, 3) - 0.106 * math.pow(Cl, 2) + 0.05059 * Cl + 0.01292
    elif M <= 0.4:
        Cd0 = 0.1266 * math.pow(Cl, 3) - 0.106 * math.pow(Cl, 2) + 0.05059 * Cl + 0.01292
        Cd1 = 0.1266 * math.pow(Cl, 3) - 0.1041 * math.pow(Cl, 2) + 0.04954 * Cl + 0.01317
        Cd = Cd0 + 10 * (M - 0.3) * (Cd1 - Cd0)
    elif M <= 0.5:
        Cd0 = 0.1266 * math.pow(Cl, 3) - 0.1041 * math.pow(Cl, 2) + 0.04954 * Cl + 0.01317
        Cd1 = 0.1266 * math.pow(Cl, 3) - 0.1022 * math.pow(Cl, 2) + 0.0485 * Cl + 0.01341
        Cd = Cd0 + 10 * (M - 0.4) * (Cd1 - Cd0)

    elif M <= 0.6:
        Cd0 = 0.1266 * math.pow(Cl, 3) - 0.1022 * math.pow(Cl, 2) + 0.0485 * Cl + 0.01341
        Cd1 = 0.1266 * math.pow(Cl, 3) - 0.09995 * math.pow(Cl, 2) + 0.04729 * Cl + 0.0137
        Cd = Cd0 + 10 * (M - 0.5) * (Cd1 - Cd0)
    elif M <= 0.7:
        Cd0 = 0.1266 * math.pow(Cl, 3) - 0.09995 * math.pow(Cl, 2) + 0.04729 * Cl + 0.0137
        Cd1 = 0.1266 * math.pow(Cl, 3) - 0.09615 * math.pow(Cl, 2) + 0.04533 * Cl + 0.01416
        Cd = Cd0 + 10 * (M - 0.6) * (Cd1 - Cd0)
    elif M <= 0.74:
        Cd0 = 0.1266 * math.pow(Cl, 3) - 0.09615 * math.pow(Cl, 2) + 0.04533 * Cl + 0.01416
        Cd1 = 0.09975 * math.pow(Cl, 3) - 0.06267 * math.pow(Cl, 2) + 0.03299 * Cl + 0.01562
        Cd = Cd0 + 25 * (M - 0.7) * (Cd1 - Cd0)
    elif M <= 0.76:
        Cd0 = 0.09975 * math.pow(Cl, 3) - 0.06267 * math.pow(Cl, 2) + 0.03299 * Cl + 0.01562
        Cd1 = 0.1511 * math.pow(Cl, 3) - 0.1213 * math.pow(Cl, 2) + 0.05378 * Cl + 0.01348
        Cd = Cd0 + 50 * (M - 0.74) * (Cd1 - Cd0)
    elif M <= 0.77:
        Cd0 = 0.1511 * math.pow(Cl, 3) - 0.1213 * math.pow(Cl, 2) + 0.05378 * Cl + 0.01348
        Cd1 = 0.1762 * math.pow(Cl, 3) - 0.1491 * math.pow(Cl, 2) + 0.06349 * Cl + 0.01255
        Cd = Cd0 + 100 * (M - 0.76) * (Cd1 - Cd0)
    elif M <= 0.78:
        Cd0 = 0.1762 * math.pow(Cl, 3) - 0.1491 * math.pow(Cl, 2) + 0.06349 * Cl + 0.01255
        Cd1 = 0.2363 * math.pow(Cl, 3) - 0.2121 * math.pow(Cl, 2) + 0.08388 * Cl + 0.01067
        Cd = Cd0 + 100 * (M - 0.77) * (Cd1 - Cd0)
    elif M <= 0.79:
        Cd0 = 0.2363 * math.pow(Cl, 3) - 0.2121 * math.pow(Cl, 2) + 0.08388 * Cl + 0.01067
        Cd1 = 0.2796 * math.pow(Cl, 3) - 0.255 * math.pow(Cl, 2) + 0.09696 * Cl + 0.009634
        Cd = Cd0 + 100 * (M - 0.78) * (Cd1 - Cd0)


    return Cd

# 计算空气密度
def computer_Air_density(H):
    row0 = 1.225;
    T0 = 288.15;
    h = H / 3.2808; # 英尺换米
    if h <= 1000:
        row = 1.112 + ((1000-h)/1000*(1.225-1.112))
    elif h <= 2000:
        row = 1.006 + ((2000-h)/1000*(1.112-1.006))
    elif h <= 3000:
        row = 0.909 + ((3000-h)/1000*(1.006-0.9090))
    elif h <= 4000:
        row = 0.819 + ((4000-h)/1000*(0.909-0.819))
    elif h <= 5000:
        row = 0.736 + ((5000-h)/1000*(0.819-0.736))
    elif h <= 6000:
        row = 0.66 + ((6000-h)/1000*(0.736-0.66))
    elif h <= 7000:
        row = 0.589 + ((7000-h)/1000*(0.66-0.589))
    elif h <= 8000:
        row = 0.525 + ((8000-h)/1000*(0.589-0.525))
    elif h <= 9000:
        row = 0.466 + ((9000-h)/1000*(0.525-0.466))
    elif h <= 10000:
        row = 0.413 + ((10000-h)/1000*(0.466-0.413))
    elif h <= 11000:
        row = 0.364 + ((11000-h)/1000*(0.413-0.364))
    elif h <= 12000:
        row = 0.311 + ((12000-h)/1000*(0.364-0.311))

    return row


# def computer_dongya(H, V, S):
#     dongya = 0.102 * 0.5 * S * computer_Air_density(H) * (V*0.5144) ** 2
#     return dongya

# 爬升下降升力系数
def computer_Cl(W, XIDA, DONGYA):
    Cl = W * math.cos(XIDA/180*math.pi) / DONGYA
    return Cl

# 计算爬升所需推力
def computer_Thrust_required(XIDA, W, Cd, DONGYA):
    Fre = W * math.sin(XIDA/180*math.pi) + Cd * DONGYA
    return Fre

# 平飞所需推力计算
def computer_Thrust_curse_required(Cd, DONGYA):
    Fre1 = Cd * DONGYA
    return Fre1

# 计算相对空气密度
def computer_relative_Air_density(H):
    rho0 = 1.225;
    T0 = 288.15;
    h = H / 3.2808; # 英尺换米
    if h <= 1000:
        xida = 1.112 + ((1000-h)/1000*(1.225-1.112))
    elif h <= 2000:
        xida = 1.006 + ((2000-h)/1000*(1.112-1.006))
    elif h <= 3000:
        xida = 0.909 + ((3000-h)/1000*(1.006-0.9090))
    elif h <= 4000:
        xida = 0.819 + ((4000-h)/1000*(0.909-0.819))
    elif h <= 5000:
        xida = 0.736 + ((5000-h)/1000*(0.819-0.736))
    elif h <= 6000:
        xida = 0.66 + ((6000-h)/1000*(0.736-0.66))
    elif h <= 7000:
        xida = 0.589 + ((7000-h)/1000*(0.66-0.589))
    elif h <= 8000:
        xida = 0.525 + ((8000-h)/1000*(0.589-0.525))
    elif h <= 9000:
        xida = 0.466 + ((9000-h)/1000*(0.525-0.466))
    elif h <= 10000:
        xida = 0.413 + ((10000-h)/1000*(0.466-0.413))
    elif h <= 11000:
        xida = 0.364 + ((11000-h)/1000*(0.413-0.364))
    elif h <= 12000:
        xida = 0.311 + ((12000-h)/1000*(0.364-0.311))

    return round(xida / rho0, 4)  # 保留4位小数

# 计算平飞升力系数
def computer_curse_Cl(W, DONGYA):
    Cl = W / DONGYA
    return Cl

# 计算平飞阻力
def computer_curse_Fre(Cd0, DONGYA):
    Fre0 = Cd0 * DONGYA
    return Fre0

# 计算平下降阻力
def computer_decended_Fre(Cd, DONGYA, PITCH, W):
    Fre1 = Cd * DONGYA - W * abs(math.sin(PITCH/180*math.pi))
    return Fre1

# 计算气压、大气压强
def computer_airpressure(T):
    T0 = 288.15  # 开氏温度
    P0 = 1013.25  # 百帕
    Tk = T + 273.15  # 摄氏度转开氏温度
    p = P0 * pow((Tk / T0), 5.25588)
    return p

# 计算大气密度
def computer_airdensity(T):
    T0 = 288.15  # 开氏温度
    ROW0 = 1.225  # KG/立方米
    Tk = T + 273.15  # 摄氏度转开氏温度
    ROW = ROW0 * pow((Tk / T0), 4.25588)
    return ROW

# 计算声速
def soud_spped(T):
    T0 = 288.15  # 开氏温度
    Tk = T + 273.15  # 摄氏度转开氏温度
    a = 20.05 * pow(Tk, 0.5)
    return a

# 计算动压，空气密度与温度相关
def computer_dongya(T, S, M):
    dongya = 0.102 * 0.5 * S * computer_airdensity(T) * (((soud_spped(T)) * M) ** 2)  # 0.102牛顿转千克
    return dongya

# 计算动压，空气密度与高度相关
def computer_dongya2(H, T, S, M):
    dongya = 0.102 * 0.5 * S * computer_Air_density(H) * (((soud_spped(T)) * M) ** 2)  # 0.102牛顿转千克。修正密度，温度不合理，换成高度
    return dongya

# 计算各阶段最后的所需推力
def computer_Fe(W, Frec, Fre, Fred):
    if W >= 63004.9183:  # 高度为20000英尺前的重量
        fe = Frec
    elif W <= 56572.30179: # 高度为10000英尺后的重量
        fe = Fred
    else:
        fe = Fre
    return round(fe, 4) # 保留4位小数

# 计算各阶段最后的所需推力，第二次北京飞珠海
def computer_Fe_PEK_ZUH(W, Frec, Fre, Fred):
    if W >= 62250.62384:  # 高度为10000英尺前的重量
        fe = Frec
    elif W <= 55869.69757: # 高度为10000英尺后的重量
        fe = Fred
    else:
        fe = Fre
    return round(fe, 4) # 保留4位小数

# 计算可用推力，爬升、平飞、下降阶段
def computer_FF_aviliable(W, F0, Fclimb, Fcruise, H):
    if W >= 63538.50: # 根据燃油流量减少，判断最大连续推力前
        FF = F0 * computer_relative_Air_density(H)
    elif W >= 63580.2081: # 0.413马赫，高度5000英尺
        FF = Fclimb  # 不需进行气压密度修正
    elif W <= 56572.30179: # 高度为10000英尺后的重量
        FF = Fclimb  # 不需进行气压密度修正
    else:
        FF = Fcruise
    return round(FF, 2) # 保留2位小数

# 通过BCOP数据拟合高度的总推力关系
def computer_Total_Net_Thrust(H):
    TF = 0.10312815 * H + 17490.522
    return round(TF, 2)  # 保留2位小数

# 通过BCOP数据拟合N1总推力关系
def computer_Total_Net_Thrust_N1(N1):
    TF = 680.26336939 * N1  - 46959.2275
    return round(TF, 2)  # 保留2位小数