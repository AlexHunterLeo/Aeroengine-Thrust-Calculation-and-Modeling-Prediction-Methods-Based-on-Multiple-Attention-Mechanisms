# 计算第二次北京飞珠海， 4/11/2012 Frame Layout: Format: All Parameters" (v1.00)"
# Flight: 1323-0 PEK-ZUH T/O Frm: 585   6:41:00 AM GMT   62705 KGS Lnd Frm: 3407   9:50:00 AM GMT   55483 KGS
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
# %matplotlib inline

from compute_L_D import *

"""
本程序可能需要调的地方：
1）取不同阶段的所需推力，起飞过程中将20000英尺以下定为爬升；
下降过程将10000英尺以下定为下降，其余按照平飞计算
"""



#设置绘图大小
plt.style.use({'figure.figsize':(25,20)})

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
raw_data = pd.read_csv('LD224.csv',sep=',')

# 机翼面积
S = 125
# 节换米每秒
k1 = 0.5144
# 牛换千克
k2 = 0.102
# 海平面标压推力
F0 = 0.45359237 * 27300 * 2
# 最大连续爬升推力
F1 = 0.45359237 * 20709 * 2

M = raw_data['MACH']  # 马赫数
H = raw_data['ALTSTD']  # 气压高
V = raw_data['AIRSPD'] # 计算空速
W = raw_data['W'] # 飞机重量
XIDA = raw_data['XIDA'] # 姿态角，爬升姿态是俯仰角减去攻角，下降姿态是攻角加俯仰角
PITCH = raw_data['PITCH']  # 飞机俯仰角
N1 = raw_data['N1']  # 低压转子
T = raw_data['T']  # 总温

# DONGYA = raw_data['DONGYA']  # 计算动压
# Cl = raw_data['Cl']  # 起飞爬升下降升力系数
# Cd = raw_data['Cd']  # 起飞爬升下降阻力系数
# Cl0 = raw_data['Cl0']  # 平飞升力系数
# Cd0 = raw_data['Cd0']  # 平飞阻力系数
# H = np.array(H)
# Cl2 = raw_data['Cl2']  # 更新后，起飞爬升升力系数
# Cd2 = raw_data['Cd2']  # 更新后，起飞爬升阻力系数
#
# DONGYA3 = raw_data['DONGYA3']

# 计算动压
b1 = []
for i in range(len(M)):
    a = computer_dongya2(float(H[i]), float(T[i]), S, float(M[i]))
    b1.append(a)
raw_data['DONGYA2'] = b1
#

# 计算平飞升力系数
b2 = []
for i in range(len(M)):
    a = computer_curse_Cl(float(W[i]), float(b1[i]))  # 重量、动压
    b2.append(a)
raw_data['Cl'] = b2

# 计算平飞阻力系数
b3 = []
for i in range(len(M)):
    a = computer_Cd_polarcurve(float(M[i]), float(b2[i]))  # 马赫数、升力系数
    b3.append(a)
raw_data['Cd'] = b3

# 计算爬升、下降阶段升力系数
b5=[]
for i in range(len(M)):
    a = computer_Cl(float(W[i]), float(XIDA[i]), float(b1[i]))  # 重量、航迹角、动压
    b5.append(a)
raw_data['Clcd'] = b5

# 计算爬升、下降阻力系数
b6 = []
for i in range(len(M)):
    a = computer_Cd_polarcurve(float(M[i]), float(b5[i]))  # 马赫数、升力系数
    b6.append(a)
raw_data['Cdcd'] = b6

# 计算平飞所需推力
b4 = []
for i in range(len(M)):
    a = computer_curse_Fre(float(b3[i]), float(b1[i])) # 阻力系数、动压
    b4.append(a)
raw_data['Fre'] = b4

# 计算爬升所需推力
b7 = []
for i in range(len(M)):
    a = computer_Thrust_required(float(XIDA[i]), float(W[i]), float(b6[i]), float(b1[i])) # 航迹角、重量、爬升阻力系数、动压
    b7.append(a)
raw_data['Frec'] = b7 # 爬升所需推力

# 计算下降所需推力
b8 = []
for i in range(len(M)):
    a = computer_decended_Fre(float(b6[i]), float(b1[i]), float(XIDA[i]), float(W[i]))  # 下降阻力系数、动压、航迹角、重量
    b8.append(a)
raw_data['Fred'] = b8

# 各阶段所需推力总结
b9 = []
for i in range(len(M)):
    a = computer_Fe_PEK_ZUH(float(W[i]), float(b7[i]), float(b4[i]), float(b8[i]))
    b9.append(a)
raw_data['Fe'] = b9  # 各阶段所需推力

# # 各阶段最大推力
# b10 = []
# for i in range(len(M)):
#     a = computer_FF_aviliable(float(W[i]), F0, Fclimb, Fcruise, float(H[i]))  # computer_FF_aviliable(W, F0, Fclimb, Fcruise, H):
#     b10.append(a)
# raw_data['FF'] = b10
#
# # 拟合曲线后，依据高度拟合，计算的总推力
# b11 = []
# for i in range(len(M)):
#     a = computer_Total_Net_Thrust(float(H[i]))
#     b11.append(a)
# raw_data['TF'] = b11
#
#
# # 拟合曲线后，采用N1计算的总推力
# b12 = []
# for i in range(len(M)):
#     a = computer_Total_Net_Thrust_N1(float(N1[i]))
#     b12.append(a)
# raw_data['TF_N1'] = b12

# 采用起飞推力27300磅，最大连续爬升20709磅计算最大推力，依照相对气压密度修正推力
b13 = []
for i in range(len(M)):
    if float(W[i]) > 62331.6489:   # 两百秒对应重量
        a = F0 * computer_relative_Air_density(float(H[i]))
    else:
        a = F1 * computer_relative_Air_density(float(H[i]))
    b13.append(a)
raw_data['Thrust_H'] = b13

raw_data.to_csv("LD229.csv")
print("6" * 6)

# y=raw_data["Cd0.79"]
# y=y[0:23]
# x=raw_data["0.79"]
# x=x[0:23]
# #
# for i in range(len(y)):
#     print(y[i])
