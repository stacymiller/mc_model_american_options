import numpy as np
from scipy.stats import norm

from constants import *
from quazi_mc_seq_gen import HaltonNorm

ticks = 0


def value(state):
    return np.max(state)


def payoff(state):
    return max(value(state) - K, 0)


def get_states(state, n):
    size = (n,) + np.asarray(state).shape
    if type == "pseudorandom":
        rand = norm.rvs(size=size)
    elif type == "quasirandom":
        rand = quasirand.gaussian(size=size)
    else:
        raise ValueError("type \"{}\" is wrong!".format(type))
    return state * np.exp((mu - sigma * sigma / 2) * deltat +
                          sigma * np.sqrt(deltat) * rand.dot(corr_matrix))


def evaluate_tree(state, branches, steps_left):
    if steps_left == 0:
        # print(" " * (m - steps_left), payoff(state))
        return payoff(state), payoff(state)
    children = get_states(state, branches)
    contin_values = []
    for child in children:
        contin_values.append(evaluate_tree(child, branches, steps_left - 1))
    contin_values = np.array(contin_values)
    upper_contin_values = contin_values[:, 0]
    lower_contin_values = contin_values[:, 1]

    p = payoff(state)
    est_upper = max(p, discount * np.mean(upper_contin_values))
    est_lower = np.where(lower_contin_values.mean() - lower_contin_values < p, p, lower_contin_values).mean()
    # print(" " * (m - steps_left), max(payoff(state), discount * est))
    return est_upper, est_lower

np.random.seed(13)
# print(evaluate_tree(S0, 4, m))
# values = [evaluate_tree(S0, 50, m) for _ in range(100)]
# print(np.mean(values))
# print(np.std(values))

samples=500
quasirand = HaltonNorm(10)
fmt = "{S0},{rho},{K},{m},{b},{est_upper},{est_lower},{type},{halton_dim}\n"
# with open("results_continious.csv", "w") as f:
#     f.write("S0,rho,K,m,b,est,type,halton_dim\n")
for branches in [10,20,50,100]:#, 150, 200, 300]:
    b = branches
    print("{S0},{rho},{K},{m},{b},{type}\n".format(S0=np.mean(S0), rho=rho, K=K, m=m, b=b, type=type))
    f = open("results_continious_{branches}.csv".format(branches=branches), "w")
    f.write(fmt.format(S0="S0", rho="rho", K="K", m="m", b="b",
                       est_upper="est_upper", est_lower="est_lower", type="type", halton_dim="halton_dim"))
    for type in ["quasirandom", "pseudorandom"]:
        dims = [len(S0), 100, (branches**(np.arange(m) + 1)).sum()] if type == "quasirandom" else [None]
        for halton_dim in dims:
            if halton_dim is not None:
                if halton_dim > 1200:
                    continue
                quasirand = HaltonNorm(int(halton_dim), cache=10000, randomized=True)
            print(branches, type, halton_dim)
            # f = open("results_continious_{branches}_{type}_{dim}.csv".format(branches=branches, type=type, dim=halton_dim), "w")
            strata = 10
            for i in range(samples):
                # print(i)
                if (i // (samples / strata)) != (i - 1) // (samples / strata):
                    quasirand.randomize()
                upper, lower = evaluate_tree(S0, b, m)
                f.write(fmt.format(
                    S0=np.mean(S0), rho=rho, K=K, m=m, b=b, est_upper=upper, est_lower=lower, type=type, halton_dim=halton_dim
                ))
    f.close()
