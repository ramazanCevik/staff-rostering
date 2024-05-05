# coding: utf-8

import random
import json
import numpy as np
import pickle
np.random.seed(460)
random.seed(460)



location = "./data/"



sets = {"G": ["loc1", "loc2", "loc3"],
        "R": ["shift1", "shift2", "shift3","shift4"], 
        "O": ["o1"], 
        "T": [*range(1,25)], 
        "D": [*range(1,8)],
        "V": ["v1", "v2"], 

        "S": ["s1", "s2", "s3"]}

with open(location+"sets.json","w") as f:
    sets["A"] = [*range(8)]
    json.dump(sets, f)
print(sets)



c_vgtd = {}
for v in sets["V"]:
    c_vgtd[v]={}
    for g in sets["G"]:
        c_vgtd[v][g]={}
        for t in sets["T"]:
            c_vgtd[v][g][t]={}
            for d in sets["D"]:
                c_vgtd[v][g][t][d]={}
                c_vgtd[v][g][t][d] = random.randint(2,9)


u_std = {}
for s in sets["S"]:
    u_std[s]={}
    for t in sets["T"]:
        u_std[s][t]={}
        for d in sets["D"]:
            u_std[s][t][d]= random.randint(5,10)


r_std = {}
for s in sets["S"]:
    r_std[s]={}
    for t in sets["T"]:
        r_std[s][t]={}
        for d in sets["D"]:
            r_std[s][t][d]= random.randint(5,10) # TODO: implement



p_as = {}
for a in sets["A"]:
    p_as[a] = {}
    for s in sets["S"]:
        p_as[a][s] = int(np.random.choice([1,0]))
        



l_ag = {}
for a in sets["A"]:
    l_ag[a] = {}
    for g in sets["G"]:
        l_ag[a][g] = int(np.random.choice([1,0]))


K_v = {v:int(np.random.choice([3,15])) for v in sets["V"]}


meta_parameters = {
"eta" : 5,
"teta" : 6 ,# by law
"tau_max" :5, # case
"tau" :5, # case
"beta" : 56, #by law
"gamma_max" : 40,
"gamma_min": 10,
        "n": 2,
    "m":len(sets["D"]) ,
"o":4}


a_day_d = {}
for a in sets["A"]:
    a_day_d[a] = {}
    for d in sets["D"]:
        a_day_d[a][d] = random.randint(1,10)
    



a_shf_w = {}

for a in sets["A"]:
    a_shf_w[a] = {}
    for w in sets["R"]+sets["O"]:
        a_shf_w[a][w] = random.randint(1,10)



a_a = {a:random.randint(1,10) for a in sets["A"]}

shifts_ = {"shift1":(0,9),"shift2":(9,18),"shift3":(9,20),"shift4":(15,24),"o1":(15,24),
}

e_wt = {w:{t:1*(shifts_[w][0]<=t and shifts_[w][1]>=t) for t in sets["T"]} for w in sets["R"]+sets["O"]} 
b_wt = {w:{t:1*(shifts_[w][0]==t) for t in sets["T"]} for w in sets["R"]+sets["O"]} 
f_wt = {w:{t:1*(shifts_[w][1]==t) for t in sets["T"]} for w in sets["R"]+sets["O"]} 
h_w = {w:sum([*e_wt[w].values() ]) for w in sets["R"]+sets["O"]} 
y_w1_w2 = { w1:{w2:1*(24+shifts_[w2][0]-shifts_[w1][1]>11) for w2 in sets["R"]+sets["O"]} for w1 in sets["R"]+sets["O"]}



data = {}
for i in dir():
    if isinstance(eval(i),dict) and i[0]!="_" and i!="Out" and i!="data":
        data[i] = eval(i)




with open(location+"data.pickle","bw") as f:
    pickle.dump(data,f)
print(data)

