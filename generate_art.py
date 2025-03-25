#!/usr/bin/env python3
# generate_art.py
# -*- coding: utf-8 -*-  # 

import matplotlib.pyplot as plt
import numpy as np

# 生成随机艺术图案
plt.figure(figsize=(10, 10))
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x**2 + np.random.rand(100))
plt.plot(x, y)
plt.savefig("art.png")
print("Art generated: art.png")