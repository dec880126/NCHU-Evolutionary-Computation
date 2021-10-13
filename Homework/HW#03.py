"""
 # Evolutionary Computation HW #02

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
    plt.title("Normal (Gaussian) distribution")
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

print("[*]" + "Evolutionary Computation HW #03".center(50, "="))
print("[*]Student ID:\t7110064490")
print("[*]Name:\tHuang Sin-Cyuan(黃新荃)")
print("[*]")

print("[*]" + "Description".center(50, "="))
print("""[*]\tIn this HW, use the built-in random number class
[*]in Python to generate random number sequences, then
[*]view their distributions using matplotlib""")
print("[*]")

print("[*]" + "Question List".center(50, "="))
print("[>]1. " + "Generate a sequence of 10,000 random real\n[*]\tnumbers on the interval [0.0, 1.0]")
print("[>]2. " + "Generate a sequence of 10,000 random real\n[*]\tnumbers with mean=5.0, stddev=2.0")
print("[>]3. " + """Make a dice-roll generator that can generate
[*]\tsummed multiple dice rolls as follows
[*]\t2d6 (2 dice rolls, 6-sided dice, sum the two dice),
[*]\t1d12 (1 dice roll, 12-sided dice),
[*]\t2d10 and 1d20.
[*]\tGenerate 10,000 trials for each case and plot the
[*]\tresulting distributions using matplotlib""")
print("[*]" + "="*50)

while True:
    try:
        solutionNum = int(input("[?]Please enter the index of the answer you want to check: "))
        if solutionNum == 0:
            print("[*]End of the homework#03")
            break

        if solutionNum == 1:
            random_1000_real_number()
        elif solutionNum == 2:
            gaussian_distribution()
        elif solutionNum == 3:
            dice_roll_generator()
        else:
            print("[!]Please enter the index that actually exists in the above question list ! ")

        print(f"[*]You can enter 「 0 」 to finish the program...")
    except ValueError:
        print("[!]Please enter 「 integer 」 that actually exists in the above question list ! ")
