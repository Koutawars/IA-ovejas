import random

class Graph(object):
    def __init__(self, cost_matrix, rank, max_weight):
        """
        :param cost_matrix:
        :param rank: rank of the cost matrix
        """
        self.matrix = cost_matrix
        self.rank = rank
        # noinspection PyUnusedLocal
        self.pheromone = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]
        self.max_weight = max_weight
        


class ACO(object):
    def __init__(self, ant_count, generations, alpha, beta, rho, q,
                 strategy):
        """
        :param ant_count:
        :param generations:
        :param alpha: relative importance of pheromone
        :param beta: relative importance of heuristic information
        :param rho: pheromone residual coefficient
        :param q: pheromone intensity
        :param strategy: pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy

    def _update_pheromone(self, graph, ants):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    # noinspection PyProtectedMember
    def solve(self, sheep, max_weight):
        """
        :param graph:
        """
                
        best_cost = 0
        best_weight = 0
        best_solution = []
        
        rank = len(sheep)
        graph = Graph([], rank, max_weight)
                
        for gen in range(self.generations):
            # noinspection PyUnusedLocal
            ants = [_Ant(self, sheep, graph) for i in range(self.ant_count)]
            for ant in ants:
                for i in range(rank - 1):
                    ant._select_next()
                if ant.total_cost > best_cost:
                    best_cost = ant.total_cost
                    best_weight = ant.total_weight
                    best_solution = [] + ant.tabu
                # update pheromone
                ant._update_pheromone_delta()
            self._update_pheromone(graph, ants)
            print('generation #{}, best cost: {}, path: {}, weigth:{}'.format(gen, best_cost, best_solution, best_weight))
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, aco, sheep, graph):
        self.colony = aco
        self.tabu = []  # tabu list
        self.sheep = sheep
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = [i for i in range(len(sheep))]  # nodes which are allowed for the next selection
        self.eta = [[0 if i == j else 1 / sheep[j]['y'] for j in range(len(sheep))] for i in range(len(sheep))]  # heuristic information
        start = random.randint(0, len(sheep) - 1)  # start from any node
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)
        self.total_weight = sheep[start]['x']
        self.total_cost = sheep[start]['y']
        self.graph = graph

    def _select_next(self):
        denominator = 0
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta
        # noinspection PyUnusedLocal
        probabilities = [0 for i in range(self.graph.rank)]  # probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                    self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass  # do nothing
        # select next node by probability roulette
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break

        self.allowed.remove(selected)
        W = self.total_weight + self.sheep[selected]['x']
      
        if(W < self.graph.max_weight):
           self.total_cost += self.sheep[selected]['y']
           self.total_weight = W
           self.tabu.append(selected)
           self.current = selected
           

    # noinspection PyUnusedLocal
    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colony.update_strategy == 1:  # ant-quality system
                self.pheromone_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # ant-density system
                # noinspection PyTypeChecker
                self.pheromone_delta[i][j] = self.colony.Q / self.sheep[j]['y']
            else:  # ant-cycle system
                self.pheromone_delta[i][j] = self.colony.Q / self.total_cost
