import math

from aco import ACO, Graph


def main():
    sheep = []
    values = []
    cont = 0
    max_weight = 2400
    
    with open('./data/sheep_list_range2_500_arc4b.txt') as f:
        for line in f.readlines():
            if(cont >= 1):
               s = line.split(' ')
               sheep.append(dict(index=int(s[0]), x=float(s[1]), y=float(s[2])))
            cont = cont+1
               
    cost_matrix = []
    rank = len(sheep)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(sheep[j]['y'])
        cost_matrix.append(row)

    #print(cost_matrix)
        
    aco = ACO(50, 5, 1.0, 10.0, 0.5, 10, 2)
    path, cost = aco.solve(sheep, max_weight)
    print('cost: {}, path: {}'.format(cost, path))

if __name__ == '__main__':
    main()
