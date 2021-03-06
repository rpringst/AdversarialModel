# import statements
import numpy as np
import math
import random

# initial conditions
# population
paladin = 0
informant = 40
villain = 960
apathetic = 0
total = paladin + informant + villain + apathetic

w_s = 5   # witness subsample size

t = 0    # total time as given by poisson arrival process
turn = 0    # index for turns

# payoff rates for different interactions
reward = 0.3    # reward of crime
punishment = 0.6    # punishment of conviction
image = 0.2   # credibility reduction
rates = np.array([reward, punishment, image])

# population array where majority of manipulation occurs
pop = np.array([paladin, informant, villain, apathetic , total, t])

history = np.copy(pop)    # data array, keeps record of each round

def arrival():
    """Return a 1-second average Poisson Arrival Process time."""
    return -math.log(1.0 - random.random())

#ratios
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

#choosing individuals
def crim_Choice(q):
    """Returns the index (1 or 2) for the next victimizer.
    
    Keyword arguments:
    q -- population array
    """
    inf = i_R(q) / (i_R(q) + v_R(q))
    vil = v_R(q) / (i_R(q) + v_R(q))
    victimizer = np.random.choice(4, p=[0,inf,vil,0])
    return victimizer
def pop_Choice(q):
    """Returns the index (0-3) for a random individual.
    
    Keyword arguments:
    q -- population array
    """
    pal = p_R(q)
    inf = i_R(q)
    vil = v_R(q)
    ap = a_R(q)
    victim = np.random.choice(4, p=[pal,inf,vil,ap])
    return victim

#steps
def step_One(q):
    """Returns 2 indicies in an array for the victimizer and victim.
    
    Keyword arguments:
    q -- population array
    """
    vm = crim_Choice(q)
    q[vm] -= 1
    q[4] -= 1
    v = pop_Choice(q)
    q[v] -= 1
    q[4] -= 1
    return np.array([vm, v])
def step_Two(vm_v):
    """Returns whether or not a crime was reported to authorities.
    
    Keyword arguments:
    vm_v -- victimizer/victim choice array
    """
    if (vm_v[1]==2) or (vm_v[1]==3):
        return False
    else:
        return True
def step_Three(q, w):
    """Returns the indicies of the witnessing subpopulation
    
    Keyword arguments:
    q -- population array
    w -- number of witnesses to be selected
    """
    choice = pop_Choice(q)
    pop_choice = np.array([choice])
    q[choice] -= 1
    q[4] -= 1
    
    for a in range(w):
        choice = pop_Choice(q)
        pop_choice = np.append(pop_choice, np.array([choice]))
        q[choice] -= 1
        q[4] -= 1
    return pop_choice
def step_Four(witnesses):
    """Returns the number of witnesses who cooperate with investigation.
    
    Keyword arguments:
    witnesses - array of witness indicies
    """
    cooperating = 0
    for x in np.nditer(witnesses):
        if (x==0) or (x==1):
            cooperating += 1
    return cooperating
def step_Five(c, w_s):
    """Returns whether or not an investigation results in conviction
    
    Keyword arguments:
    c - number of cooperating witnesses
    w_s - total witness subpopulation size
    """
    c_p = float(c * w_s**(-1))
    conviction = np.random.choice(2, p=[c_p, (1-c_p)])
    if conviction == 0:
        return True
    else:
        return False
def step_Six(pair, reported, conviction, rates):
    payoff_vm = 1
    payoff_v = 1
    if reported==False:
        payoff_vm += rates[0]
        payoff_v -= rates[0]
    else:
        if conviction==False:
            payoff_vm += rates[0]
            payoff_v -= (rates[0] + rates[2])
        else:
            payoff_vm -= rates[1]
    payoffs = np.array([payoff_vm, payoff_v])


#to do
#perform strategy update
#bring it all together


print(step_Four(step_Three(pop, 12)))
