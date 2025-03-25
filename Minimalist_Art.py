import matplotlib.pyplot as plt
import numpy as np

def createMinimalistArt():
    # 创建一个画布
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    # 添加几个简单的几何形状
    circle = plt.Circle((5, 5), 2, color='blue', fill=False)
    rectangle = plt.Rectangle((2, 2), 3, 3, color='red', fill=False)
    triangle = plt.Polygon([[6, 2], [8, 4], [7, 6]], color='green', fill=False)

    ax.add_artist(circle)
    ax.add_artist(rectangle)
    ax.add_artist(triangle)

    # 显示图像
    #plt.show()

    plt.savefig("art.png")
print("Art generated: art.png")

createMinimalistArt()