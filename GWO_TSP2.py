

def find_next_wolfs(population, matx):
    lst_check = population.copy()
    last_point = population[-1]

    # find alpha point
    alpha_point = 9999
    alpha_min = 9999
    for i in range(len(matx)):
        if i not in lst_check and matx[last_point][i] < alpha_min:
            alpha_point = i
            alpha_min = matx[last_point][i]
    lst_check.append(alpha_point)

    # find beta_point
    beta_point = 9999
    beta_min = 9999
    for i in range(len(matx)):
        if i not in lst_check and matx[last_point][i] < beta_min:
            beta_point = i
            beta_min = matx[last_point][i]
    lst_check.append(beta_point)

    # find delta_point
    delta_point = 9999
    delta_min = 9999
    for i in range(len(matx)):
        if i not in lst_check and matx[last_point][i] < delta_min:
            delta_point = i
            delta_min = matx[last_point][i]
    lst_check.append(alpha_point)

    return alpha_point, beta_point, delta_point


def find_wolf(population, lst_check, matx):
    # return to start point
    if len(population) == len(matx):
        return population[0]
    if len(population) > len(matx):
        return 9999

    last_point = population[-1]

    # find next point
    next_point = 9999
    next_min = 9999
    for i in range(len(matx)):
        if i not in lst_check:
            if matx[last_point][i] < next_min:
                next_point = i
                next_min = matx[last_point][i]
    return next_point


def reformat_population(population, population_size):
    lst = population.copy()
    lst.sort(key=lambda x: x[1])
    # print("lst: ", lst)
    max_value = lst[population_size][1]
    # print("max_value: ", max_value)
    new_list = [x for x in population if x[1] < max_value]
    # print("new_list: ",new_list)

    return new_list


def GWO_TSP2(path_value, t):
    matx = path_value
    # prey_size = 3
    n = len(path_value)
    population_size = n + 1
    population = []
    population.append([[t], 0])
    count = 1
    while len(population) <= population_size and count < population_size:
        top_population = population[0].copy()
        while len(top_population[0]) == count:

            alpha_population = top_population.copy()
            beta_population = top_population.copy()
            delta_population = top_population.copy()
            check_population = top_population[0].copy()
            population.remove(top_population)
            # print(population)

            # update alpha
            x_alpha = find_wolf(alpha_population[0], check_population, matx)
            if x_alpha < 100:
                alpha_population[1] += matx[alpha_population[0][-1]][x_alpha]
                alpha_population[0] = alpha_population[0] + [x_alpha]
                population.append([alpha_population[0], alpha_population[1]])
                check_population.append(x_alpha)

            # update beta
            x_beta = find_wolf(beta_population[0], check_population, matx)
            if x_beta == x_alpha:
                x_beta = 9999
            if x_beta < 100:
                beta_population[1] += matx[beta_population[0][-1]][x_beta]
                beta_population[0] = beta_population[0] + [x_beta]
                population.append([beta_population[0], beta_population[1]])
                check_population.append(x_beta)

            # update delta
            x_delta = find_wolf(delta_population[0], check_population, matx)
            if x_delta == x_alpha:
                x_delta = 9999
            if x_delta < 100:
                delta_population[1] += matx[delta_population[0][-1]][x_delta]
                delta_population[0] = delta_population[0] + [x_delta]
                population.append([delta_population[0], delta_population[1]])

            # print(x_alpha, x_beta, x_delta)
            top_population = population[0].copy()


        if len(population) > population_size:
            population = reformat_population(population, population_size)
            #print(len(population))
        #print(population)
        count += 1

    population.sort(key=lambda x: x[1])
    return population[0]


def run_GWO(path_value):
    # lst = [[0, 34,50756334578302, 22.854323573670655, 33.133881472831305, 32.44642041709688, 32.29077171568983, 41.32745363200192, 34.60589997533138, 33.47327581167178, 33.36414353639994],
    #        [34.50756334578302, 0.0, 38.78526567957931, 27.14678426375078, 24.976164104481533, 39.88816151428006, 35.75919464567039, 35.344578366931536, 40.08687419857077, 32.961942356847985],
    #        [22.854323573670655, 38.78526567957931, 0.0, 45.84955456018835, 24.58090178664591, 35.772531974959925, 41.319011454574905, 27.190815290383252, 31.940434534984426, 39.56307056885795],
    #        [33.133881472831305, 27.14678426375078, 45.84955456018835, 0.0, 32.88685893405129, 32.09656022348861, 33.96111295709401, 47.0656728596857, 29.831942693779794, 31.277746354553134],
    #        [32.44642041709688, 24.976164104481533, 24.58090178664591, 32.88685893405129, 0.0, 38.457613174525484, 35.93499801770572, 31.71573745206073, 31.490184659670156, 36.00604303147982],
    #        [32.29077171568983, 39.88816151428006, 35.772531974959925, 32.09656022348861, 38.457613174525484, 0.0, 30.396645871185164, 35.84222349439915, 36.55583525828927, 25.88385368553901],
    #        [41.32745363200192, 35.75919464567039, 41.319011454574905, 33.96111295709401, 35.93499801770572, 30.396645871185164, 0.0, 32.12173391538704, 33.46664896531891, 34.70521173290715],
    #        [34.60589997533138, 35.344578366931536, 27.190815290383252, 47.0656728596857, 31.71573745206073, 35.84222349439915, 32.12173391538704, 0.0, 37.16273254233167, 25.19904764705158],
    #        [33.47327581167178, 40.08687419857077, 31.940434534984426, 29.831942693779794, 31.490184659670156, 36.55583525828927, 33.46664896531891, 37.16273254233167, 0.0, 23.16907986026424],
    #        [33.36414353639994, 32.961942356847985, 39.56307056885795, 31.277746354553134, 36.00604303147982, 25.88385368553901, 34.70521173290715, 25.19904764705158, 23.16907986026424, 0.0]]

    lst = path_value
    n = len(lst)
    best_result = []
    best_cost_result = 99999
    for i in range(1, 4):
        t = round(n*i/4)
        result = GWO_TSP2(lst, t)
        if result[1] < best_cost_result:
            best_result = result[0]
            best_cost_result = result[1]
    return [best_result, best_cost_result]
    # print(result[0])
    # print(result[1])


# run_GWO()