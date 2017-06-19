# import statements
import numpy as np
import math
import random
from tempfile import TemporaryFile
outfile = TemporaryFile()

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
    if i_R(q)==0 and v_R(q)==0:
        return 4
    else:
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
    tot = pal + inf + vil + ap
    victim = np.random.choice(4, p=[pal/tot,inf/tot,vil/tot,ap/tot])
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
    
    for a in range(w-1):
        choice = pop_Choice(q)
        pop_choice = np.append(pop_choice, np.array([choice]))
        q[choice] -= 1
        q[4] -= 1
    return pop_choice
def step_Four(witnesses):
    """Returns the number of witnesses who cooperate with investigation.
    
    Keyword arguments:
    witnesses -- array of witness indicies
    """
    cooperating = 0
    for x in np.nditer(witnesses):
        if (x==0) or (x==1):
            cooperating += 1
    return cooperating
def step_Five(c, w_s):
    """Returns whether or not an investigation results in conviction.
    
    Keyword arguments:
    c -- number of cooperating witnesses
    w_s -- total witness subpopulation size
    """
    c_p = float(c * w_s**(-1))
    c_pp = 1 - c_p
    if (c_pp<0):
        print(c)
        print(c_p)
        print("Error!!!!")
    conviction = np.random.choice(2, p=[c_p, c_pp])
    if conviction == 0:
        return True
    else:
        return False
def step_Six(reported, conviction, rates):
    """Returns the associated payoffs of the victimizer and victim
    
    Keyword arguments:
    reported -- Boolean for whether or not crime was reported
    conviction -- Boolean for whether or not the victimizer was convicted
    rates -- the associated payoff rates for different actions
    """
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
    return payoffs
def step_Seven(vm_v, scores):
    tot = 0
    for x in np.nditer(scores):
        tot += x
    update = np.random.choice(2, p=[float(scores[0]*tot**(-1)),float(scores[1]*tot**(-1))])
    if update==0:
        return vm_v[0]
    else:
        if vm_v[1]==0 or vm_v[1]==1:
            return 0
        else:
            return 3

#to do
#bring it all together
for k in range(25):
    # initial conditions
    # population
    paladin = 50.0
    informant = 400.0
    villain = 1600.0
    apathetic = 20.0
    total = paladin + informant + villain + apathetic

    w_s = 5  # witness subsample size

    t = 0.0    # total time as given by poisson arrival process
    turn = 0    # index for turns

    # payoff rates for different interactions
    reward = 0.5    # reward of crime
    punishment = 0.5    # punishment of conviction
    image = 0.1   # credibility reduction
    payoff = np.array([reward, punishment, image])

    # population array where majority of manipulation occurs
    pop = np.array([paladin, informant, villain, apathetic , total, t, turn])

    history = np.copy(pop)    # data array, keeps record of each round
    yada = False
    while yada==False:
        pop[6] += 1
        pop[5] += arrival()
        if ((pop[0]==0) and (pop[1]==0) or ((pop[2]==0) and (pop[3]==0))):
            break
        else:
            working_pop = np.copy(pop)
            #print(pop)
            x = step_One(working_pop)
            if x[0]==4:
                break
            #print(x)
            y = step_Two(x)
        #print(y)
            z = step_Six(y, step_Five(step_Four(step_Three(working_pop, w_s)), w_s), payoff)
        #print(z)
            h = step_Seven(x, z)
        #print(h)
            if z[0] < z[1]:
                pop[x[0]] -= 1
            else:
                  pop[x[1]] -= 1
            pop[h] += 1
            history = np.vstack([history, pop])
            if ((pop[0]==0) and (pop[1]==0) or ((pop[2]==0) and (pop[3]==0))):
                yada==True
    print(history)
    title = str(k)
    np.savetxt((title + "history.npy"), history, fmt='%7f', delimiter=' ')

