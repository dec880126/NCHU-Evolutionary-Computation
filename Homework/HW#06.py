"""
 # Evolutionary Computation HW #06
 # Binary tournament selection experiment

 - Student ID: 7110064490
 - Name: Huang Sin-Cyuan(黃新荃)
 - Email: dec880126@icloud.com
"""
from random import Random
import matplotlib.pyplot as plt

# A few useful constants
#
pop_size = 20
generations = 10
fit_range = 40

# Init the random number generator
#
prng = Random()
prng.seed(123)


# Let's suppose we have an imaginary problem that generates
# integer fitness values on some fixed range.  We'll start by randomly
# initializing a population of fitness values
#
pop = [prng.randrange(0,fit_range) for i in range(pop_size)]


def plt_hist(pop, bin_limit=fit_range):
    """
    Plot histogram of population fitness values
    """
    plt.hist(pop, bins=range(0,bin_limit+1))
    plt.grid(True)
    plt.title('Distribution of Population')
    plt.show()
    
def binary_tournament(pop_in: list, prng: Random):
    """
    Binary tournament operator:
    - Input: population of size N (pop_size)
    - Output: new population of size N (pop_size), the result of applying selection

    - Tournament pairs should be randomly selected
    - All individuals from input population should participate in exactly 2 tournaments
    """
    print(f"[>]{pop_in[0]} v.s {pop_in[1]} -> Winner is {max(pop_in)}")
    
    pop_in.remove(min(pop_in))

    return pop_in


# Let's iteratively apply our binary selection operator
# to the initial population and plot the resulting fitness histograms.
# This is somewhat like having a selection-only EA without any stochastic variation operators
#
competitors = []
print(f'[*]Initial Population: {pop}')
for gen in range(generations):
    competitors.append(prng.choices(pop, k = 2))
plt_hist(pop)

new_pop = []
for _competitors in competitors:
    new_pop.append(binary_tournament(_competitors, prng)[0])
plt_hist(new_pop)

print(new_pop)
