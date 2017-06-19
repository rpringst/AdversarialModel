# import statements
import numpy as np

# initial conditions
# population
paladin = 0
informant = 40
villain = 960
apathetic = 0
total = paladin + informant + apathetic + villain

# witness subsample size
w_s = 5

time = 0    # total time as given by poisson arrival process
turn = 0    # index for turns

# payoff rates for different interactions
reward = 0.3    # reward of crime
punishment = 0.6    # punishment of conviction
image = 0.2   # credibility reduction

# population array where majority of manipulation occurs
pop = np.array([paladin, informant, villain, apathetic , total, time])

history = np.copy(pop)    # data array, keeps record of each round

def arrival():
    """Return a 1-second average Poisson Arrival Process time."""
    ar = np.random.poisson(10, 1) * 0.1
    return ar

def p_R(q):
    """Returns ratio of Paladins to total population.
    
    Keyword arguments:
    q -- population array
    """
    return float(q[0] * q[4]**(-1))
def i_R(q):
    """Returns ratio of Informants to total population.
    
    Keyword arguments:
    q -- population array
    """
    return float(q[1] * q[4]**(-1))
def v_R(q):
    """Returns ratio of Villains to total population.
    
    Keyword arguments:
    q -- population array
    """
    return float(q[2] * q[4]**(-1))
def a_R(q):
    """Returns ratio of Apathetics to total population.
    
    Keyword arguments:
    q -- population array
    """
    return float(q[3] * q[4]**(-1))

#takes in current population q and returns the index in the population
#vector for the next criminal
def crim_Choice(q):
    inf = i_R(q) / (i_R(q) + v_R(q))
    vil = v_R(q) / (i_R(q) + v_R(q))
    victimizer = np.random.choice(4, p=[0,inf,vil,0])
    return victimizer

#takes in current population q and returns the index in the population
#vector for a random individual
def pop_Choice(q):
    pal = p_R(q)
    inf = i_R(q)
    vil = v_R(q)
    ap = a_R(q)
    victim = np.random.choice(4, p=[pal,inf,vil,ap])
    return victim

#takes in the current population q and returns an array of the victimizer
#and victim choices as indicies of the population vector
def step_One(q):
    vm = crim_Choice(q)
    q[vm] -= 1
    q[4] -= 1
    v = pop_Choice(q)
    q[v] -= 1
    q[4] -= 1
    return np.array([vm, v])

#accepts an array of indicies to check if a crime is reported
def step_Two(v_vm):
    if (v_vm[1]==2) or (v_vm[1]==3):
        return False
    else:
        return True

#accepts an array of the remaining N - 2 population, the number of witnesses,
#and returns an array of the witnessing subpopulation
def step_Three(q, w):
    pop_choice = np.array([pop_Choice(q)])
    for a in range(w-1):
        pop_choice = np.append(pop_choice, np.array([pop_Choice(q)]))
    return pop_choice

print(step_Two(step_One(pop)))
print(pop)
print(step_Three(pop, w_s))
print(pop)
print(history)
