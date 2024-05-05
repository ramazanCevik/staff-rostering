
from pyomo.environ import *



location = "./data/"



def solve_rostering_problem(data):
    sets = data["sets"]
    meta_parameters = data["meta_parameters"]
    m = ConcreteModel()
    m.x = Var(sets["A"],sets["R"]+sets["O"],sets["D"],within=Binary)
    m.I = Var(sets["V"],sets["G"],sets["T"],sets["D"],within=NonNegativeIntegers)
    m.L = Var(sets["V"],sets["G"],sets["T"],sets["D"],within=NonNegativeIntegers)
    m.U = Var(sets["S"],sets["T"],sets["D"], within=NonNegativeReals)
    o = meta_parameters["o"]
    c_vgtd = data["c_vgtd"]
    u_std = data["u_std"]
    m.obj1 = Objective(expr=
        sum([sum([sum([o*m.x[a,w,d] for d in sets["D"]]) for w in sets["O"]]) for a in sets["A"]])
        +sum([sum([sum([sum([c_vgtd[v][g][t][d]*(m.I[v,g,t,d]+m.L[v,g,t,d]) for v in sets["V"]]) for g in sets["G"]])  for t in sets["T"]]) for d in sets["D"]])
        +sum([sum([sum([u_std[s][t][d]*m.U[s,t,d] for s in sets["S"]]) for t in sets["T"]]) for d in sets["D"]]), sense=minimize
        )



    m.constraint2 = ConstraintList()
    l_ag = data["l_ag"]
    b_wt = data["b_wt"]
    K_v = data["K_v"]
    for g in sets["G"]:
        for t in sets["T"]:
            for d in sets["D"]:
                m.constraint2.add(
                sum([ sum(l_ag[a][g]*b_wt[w][t]*m.x[a,w,d]  for w in sets["R"]+sets["O"] )    for a in sets["A"] ])
                <=sum([K_v[v]*m.I[v,g,t,d] for v in sets["V"]]) )



    m.constraint3 = ConstraintList()
    f_wt = data["f_wt"]
    for g in sets["G"]:
        for t in sets["T"]:
            for d in sets["D"]:
                m.constraint3.add(
                sum([ sum(l_ag[a][g]*f_wt[w][t]*m.x[a,w,d]  for w in sets["R"]+sets["O"] )    for a in sets["A"] ])
                <=sum([K_v[v]*m.L[v,g,t,d] for v in sets["V"]]) )



    m.constraint4 = ConstraintList()
    m.P = Var(sets["A"], sets["S"], sets["R"]+sets["O"], sets["D"])
    r_std = data["r_std"]
    e_wt = data["e_wt"]
    for s in sets["S"]:
        for t in sets["T"]:
            for d in sets["D"]:
                m.constraint4.add(
                r_std[s][t][d] - sum([sum([e_wt[w][t]*m.P[a,s,w,d] for w in sets["R"]+sets["O"]]) for a in sets["A"]]) <= m.U[s,t,d]
                
                )


  

    m.constraint5 = ConstraintList()
    p_as = data["p_as"]
    for a in sets["A"]:
        for s in sets["S"]:
            for w in sets["R"]+sets["O"]:
                for d in sets["D"]:
                    m.constraint5.add(
                    m.P[a,s,w,d] <= p_as[a][s]*m.x[a,w,d]

                    )



    m.constraint6 = ConstraintList()
    for a in sets["A"]:
        for w in sets["R"]+sets["O"]:
            for d in sets["D"]:
                m.constraint6.add(
                sum([m.P[a,s,w,d] for s in sets["S"]]) <= m.x[a,w,d]
                )


    m.constraint7 = ConstraintList()
    eta = meta_parameters["eta"]
    for t in sets["T"]:
        for d in sets["D"]:
            m.constraint7.add(
            sum([  sum([e_wt[w][t]*m.x[a,w,d] for w in sets["R"]+sets["O"]]) for a in sets["A"]]) <= eta
            )



    m.constraint8 = ConstraintList()
    teta = meta_parameters["teta"]
    for a in sets["A"]:
        for d in sets["D"]:
            m.constraint8.add(
            sum([m.x[a,w,d] for w in sets["R"]+sets["O"]]) <= 1
            )


    m.constraint9 = ConstraintList()
    h_w = data["h_w"]
    m_ = meta_parameters["m"] # m is our model
    for i in range(1,m_-teta+1):# TODO: -1?
        for a in sets["A"]:
            m.constraint9.add(
            sum([sum([ m.x[a,w,d] for w in sets["R"]+sets["O"]]) for d in range(i,i+teta+1)]) <=teta  # TODO: teta?
            )


    m.constraint10 = ConstraintList()
    beta = meta_parameters["beta"]
    for i in range(1,m_-6):# TODO: -1?
        for a in sets["A"]:
            m.constraint10.add(
            sum([sum([ h_w[w]*m.x[a,w,d] for w in sets["R"]+sets["O"]]) for d in range(i,i+6+1)]) <=beta  # TODO: teta?
            )



    m.constraint11 = ConstraintList()
    y_w1_w2 = data["y_w1_w2"]
    for w1 in sets["R"]+sets["O"]:
        for w2 in sets["R"]+sets["O"]:
            for a in sets["A"]:
                m.constraint11.add(
                m.x[a,w1,d] + m.x[a,w2,d] <= y_w1_w2[w1][w2] + 1
                )

    m.constraint12= ConstraintList()
    tau = meta_parameters["tau"]
    tau_max = meta_parameters["tau_max"]
    m.W_a = Var(sets["A"], within=Binary)
    for a in sets["A"]:
        m.constraint12.add(
        sum([sum([m.x[a,w,d]-tau for d in sets["D"]]) for w in sets["R"]+sets["O"] ]) <= (tau_max-tau)*m.W_a[a]
        )
        

    m.constraint13 = ConstraintList()
    m.z_a = Var(sets["A"],within=NonNegativeReals)
    n = meta_parameters["n"]
    a_day_d = data["a_day_d"]
    a_shf_w = data["a_shf_w"]
    a_a = data["a_a"]
    for a in sets["A"]:
        m.constraint13.add(
        m.z_a[a] ==    
        sum([sum([a_day_d[a][d%7]*m.x[a,w,d]  for d in range(1,n+1)]) for w in sets["R"]+sets["O"] ])   # TODO +1
        +sum([sum([a_shf_w[a][w]*m.x[a,w,d]  for d in range(1,n+1)]) for w in sets["R"]+sets["O"] ])   
        +a_a[a]*m.W_a[a]     
        )



    m.constraint14_15 = ConstraintList()
    gamma_max = meta_parameters["gamma_max"]
    gamma_min = meta_parameters["gamma_min"]
    for a in sets["A"]:
        m.constraint14_15.add(
        m.z_a[a] <= gamma_max
        )
        m.constraint14_15.add(
        m.z_a[a] >= gamma_min
        )


    solver = SolverFactory("gurobi")


    solver.solve(m)





    UV = (1-( sum([sum([sum([m.x[a,w,d] for d in sets["D"]]) for w in sets["R"] +sets["O"]]) for a in sets["A"]]
            )/sum([K_v[v]*sum([sum([sum([(m.I[v,g,t,d]+m.L[v,g,t,d]) for d in sets["D"]]) for t in sets["T"]]) for g in sets["G"]]) for v in sets["V"]]) 
        ))*100


    OS = (sum([sum([sum(m.x[a,w,d] for a in sets["A"]) for w in sets["O"]]) for d in sets["D"]]
            )/ sum([sum([sum([m.x[a,w,d] for a in sets["A"]]) for w in sets["R"]+sets["O"]]) for d in sets["D"]]))*100



    UR = (sum([sum([sum([m.U[s,t,d] for s in sets["S"]]) for t in sets["T"]]) for d in sets["D"]]
            )/sum([sum([sum([r_std[s][t][d] for s in sets["S"]]) for t in sets["T"]]) for d in sets["D"]]))*100



    DL = sum([m.z_a[a] for a in sets["A"] ])/len([sets["A"]])

    result = {}
    result["UV%"]=value(UV)
    result["OS%"]=value(OS)
    result["UR%"]=value(UR)
    result["DL%"]=value(DL)
    result["total cost"]=value(m.obj1)
    return result