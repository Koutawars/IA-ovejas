# encoding:utf-8

# This file implements the Uniform Cost Search (UCS) algorithm
# Explanation of UCS algorithm: https://www.youtube.com/watch?v=AaKEW_mVBtg
# Author: Marcos Castro

import time
from graph import *
from priority_queue import *

TOTAL_W = 150

def create_successors(current, k):

        ind = [i for i in range(k)]
        candidates = set(ind) - set(current)
        sucessors_list = []

        for i in candidates:
            new_element = current.copy()
            new_element.append(i)
            sucessors_list.append(new_element)

        return sucessors_list

def get_weight_value(current, sheep):
        total = [0,0]
        
        for element in current:
            if element >= 0:
               total[0] = total[0] + sheep[element][1]
               total[1] = total[1] + sheep[element][2]
        return total
           
     
def run(key_node_start, goats, verbose=False, time_sleep=0):

                # UCS uses priority queue, priority is the cumulative cost (smaller cost)
                queue = PriorityQueue()
                N_sheep = len(goats)

                # expands initial node

                # get the keys of all successors of initial node
                keys_successors = create_successors(key_node_start, N_sheep)

                # adds the keys of successors in priority queue
                for key_sucessor in keys_successors:
                        w_v = get_weight_value(key_sucessor, goats)
                        
                        # each item of queue is a tuple (key, cumulative_cost)
                        if(w_v[0] <= TOTAL_W):
                             queue.insert((key_sucessor, w_v[1]), w_v[1])


                reached_goal, cumulative_cost_goal = False, -1
                
                while not queue.is_empty():

                        reached_goal = 1
                        
                        # remove item of queue, remember: item of queue is a tuple (key, cumulative_cost)
                        key_current_node, cost_node = queue.remove()
                       
                        
                        if verbose:
                                # shows a friendly message
                                print('Expands node \'%s\' with cumulative cost %s ...' % (key_current_node, cost_node))
                                w_v = get_weight_value(key_current_node, goats)
                                
                                #time.sleep(time_sleep)

                        # get all successors of key_current_node
                        keys_successors = create_successors(key_current_node, N_sheep)

                        
                        for key_sucessor in keys_successors:
                                w_v = get_weight_value(key_sucessor, goats)

                                if(w_v[0] <= TOTAL_W):
                                        
                                   cumulative_cost = w_v[1] 
                                   queue.insert((key_sucessor, cumulative_cost), cumulative_cost)

                if(reached_goal):
                        print('\nReached goal!, the best goats are: %s, Total Value: %s\n' % (key_current_node, cost_node))
                else:
                        print('\nUnfulfilled goal.\n')


if __name__ == "__main__":

      cont = 0
      sheep = [] 
      with open('./data/sheep_list_range2_500_arc4b.txt') as f:
        for line in f.readlines():
          if(cont >= 1):
            s = line.split(' ')
            sheep.append([int(s[0]), float(s[1]), float(s[2])])
          cont = cont+1
 
      current = []
      #s = create_successors(current, len(sheep))
      run(current, sheep, verbose=True, time_sleep=2)
