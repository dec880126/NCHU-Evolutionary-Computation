"""
 # Evolutionary Computation HW #03
 - Student ID: 7110064490
 - Name: Huang Sin-Cyuan(黃新荃)
 - Email: dec880126@icloud.com
"""
import numpy as np
import matplotlib.pyplot as plt

def random_1000_real_number():
    data = np.random.random((100, 100))

    plt.hist(data)
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title("10,000 random real numbers on the interval [0.0, 1.0]")
    plt.show()


def gaussian_distribution():
    # mean and standard deviation
    mean, stddev, size = 5.0, 2.0, 10000
    data = np.random.normal(mean, stddev, size)

    plt.hist(data)
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title("normal (Gaussian) distribution")
    plt.show()

def dice_roll_generator():
    min, max, size = 1, 6, 10000
    data1 = np.random.randint(low=min,high=max+1,size=size)
    data2 = np.random.randint(low=min,high=max+1,size=size)
    data = data1 + data2
    plt.subplot(2, 2, 1)
    plt.hist(data, bins=40)
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title(f"2d6")

    min, max, size = 1, 12, 10000
    data = np.random.randint(low=min,high=max+1,size=size)
    plt.subplot(2, 2, 2)
    plt.hist(data, bins=40)
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title(f"1d12")

    min, max, size = 1, 10, 10000
    data1 = np.random.randint(low=min,high=max+1,size=size)
    data2 = np.random.randint(low=min,high=max+1,size=size)
    data = data1 + data2
    plt.subplot(2, 2, 3)
    plt.hist(data, bins=40)
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title(f"2d10")

    min, max, size = 1, 20, 10000
    data = np.random.randint(low=min,high=max+1,size=size)
    plt.subplot(2, 2, 4)
    plt.hist(data, bins=40)
    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title(f"1d20")

    plt.show()



# random_1000_real_number()
# gaussian_distribution()
dice_roll_generator()
