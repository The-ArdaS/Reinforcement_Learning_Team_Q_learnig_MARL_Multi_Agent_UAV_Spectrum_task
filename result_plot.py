"""
#################################
# Load the npz file from the local drive and plot the results
#################################
"""

#########################################################
# import libraries
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter

#########################################################
# Function definition
Size_list = [2, 3, 4, 5, 6, 8, 10]
Run_list = range(0, 10)
num_Run = 10
Step_list = [120, 800, 2000, 5000, 12000, 20000, 30000]
num_Eps = 200
maximum_sum_util_grid = []
# # ********************************************************************* GRID SIZE = 2 =  2 x 2
sum_utility_size_2 = []
reward_size_2 = []
state_mat_size_2 = []
task_matrix_size_2 = []
xmat_size_2 = []
ymat_size_2 = []
action_size_2 = []
task_diff_size_2 = []
#
for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[0], Run, num_Eps, Step_list[0])
    readfile = np.load(outputFile)
    sum_utility_size_2.append(readfile['sum_utility'])


sum_sum_utility_size_2 = []
for Run in Run_list:
    sum_sum_utility_size_2.append(sum(sum_utility_size_2[Run]))

maximum_sum_util_2 = max(np.mean(sum_sum_utility_size_2, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_2)
print ('maximum_sum_util_2 = ', maximum_sum_util_2)


del readfile
del sum_utility_size_2, sum_sum_utility_size_2, reward_size_2, state_mat_size_2

# # ********************************************************************* GRID SIZE = 3 =  3 x 3
sum_utility_size_3 = []
reward_size_3 = []


for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[1], Run, num_Eps, Step_list[1])
    readfile = np.load(outputFile)
    sum_utility_size_3.append(readfile['sum_utility'])
    reward_size_3.append(readfile['reward'])

sum_sum_utility_size_3 = []
for Run in Run_list:
    sum_sum_utility_size_3.append(sum(sum_utility_size_3[Run]))

maximum_sum_util_3 = max(np.mean(sum_sum_utility_size_3, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_3)
print ('maximum_sum_util_3 = ', maximum_sum_util_3)

del readfile
del sum_utility_size_3, sum_sum_utility_size_3, reward_size_3
    
plt.close('all')
# # ********************************************************************* GRID SIZE = 4 =  4 x 4
sum_utility_size_4 = []
reward_size_4 = []
state_mat_size_4 = []
task_matrix_size_4 = []
xmat_size_4 = []
ymat_size_4 = []
action_size_4 = []
task_diff_size_4 = []
#
for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[2], Run, num_Eps, Step_list[2])
    readfile = np.load(outputFile)
    sum_utility_size_4.append(readfile['sum_utility'])

sum_sum_utility_size_4 = []
for Run in Run_list:
    sum_sum_utility_size_4.append(sum(sum_utility_size_4[Run]))

maximum_sum_util_4 = max(np.mean(sum_sum_utility_size_4, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_4)
print ('maximum_sum_util_4 = ', maximum_sum_util_4)


del readfile
del sum_utility_size_4, sum_sum_utility_size_4, reward_size_4

sum_utility_size_5 = []
reward_size_5 = []
state_mat_size_5 = []
task_matrix_size_5 = []
xmat_size_5 = []
ymat_size_5 = []
action_size_5 = []
task_diff_size_5 = []
#
for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[3],
                                                                                                          Run, num_Eps,
                                                                                                          Step_list[3])
    readfile = np.load(outputFile)
    sum_utility_size_5.append(readfile['sum_utility'])

sum_sum_utility_size_5 = []
sum_reward_size_5 = []
for Run in Run_list:
    sum_sum_utility_size_5.append(sum(sum_utility_size_5[Run]))

maximum_sum_util_5 = max(np.mean(sum_sum_utility_size_5, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_5)
print ('maximum_sum_util_5 = ', maximum_sum_util_5)

del readfile
del sum_utility_size_5, sum_sum_utility_size_5, reward_size_5

sum_utility_size_6 = []
u_fustion_size_6 = []
u_primary_size_6 = []
reward_size_6 = []
state_mat_size_6 = []
task_matrix_size_6 = []
xmat_size_6 = []
ymat_size_6 = []
action_size_6 = []
task_diff_size_6 = []
for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[4],
                                                                                                          Run, num_Eps,
                                                                                                          Step_list[4])
    readfile = np.load(outputFile)
    sum_utility_size_6.append(readfile['sum_utility'])

sum_sum_utility_size_6 = []
for Run in Run_list:
    sum_sum_utility_size_6.append(sum(sum_utility_size_6[Run]))

maximum_sum_util_6 = max(np.mean(sum_sum_utility_size_6, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_6)
print ('maximum_sum_util_6 = ', maximum_sum_util_6)


del readfile
del sum_utility_size_6, sum_sum_utility_size_6, reward_size_6


sum_utility_size_8 = []
reward_size_8 = []
state_mat_size_8 = []
task_matrix_size_8 = []
xmat_size_8 = []
ymat_size_8 = []
action_size_8 = []
task_diff_size_8 = []
#
for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[5],
                                                                                                          Run, num_Eps,
                                                                                                          Step_list[5])
    readfile = np.load(outputFile)
    sum_utility_size_8.append(readfile['sum_utility'])

sum_sum_utility_size_8 = []
for Run in Run_list:
    sum_sum_utility_size_8.append(sum(sum_utility_size_8[Run]))

maximum_sum_util_8 = max(np.mean(sum_sum_utility_size_8, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_8)
print ('maximum_sum_util_8 = ', maximum_sum_util_8)



del readfile
del sum_utility_size_8, sum_sum_utility_size_8, reward_size_8

Run_list = range(0, 5)
sum_utility_size_10 = []
reward_size_10 = []
state_mat_size_10 = []
task_matrix_size_10 = []
xmat_size_10 = []
ymat_size_10 = []
action_size_10 = []
task_diff_size_10 = []
for Run in Run_list:
    outputFile = '/data/Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size_list[6],
                                                                                                          Run, num_Eps,
                                                                                                          Step_list[6])
    readfile = np.load(outputFile)
    sum_utility_size_10.append(readfile['sum_utility'])

sum_sum_utility_size_10 = []

for Run in Run_list:
    sum_sum_utility_size_10.append(sum(sum_utility_size_10[Run]))


maximum_sum_util_10 = max(np.mean(sum_sum_utility_size_10, axis=0))
maximum_sum_util_grid.append(maximum_sum_util_10)
print ('maximum_sum_util_10 = ', maximum_sum_util_10)


del readfile
del sum_utility_size_10, sum_sum_utility_size_10, reward_size_10


plt.figure()
plt.plot(Size_list, maximum_sum_util_grid, marker='o', markersize='10', linewidth=2.0, color='blue',
         label="Maximum Utility")
plt.grid(True)
plt.ylabel('Sum Utility', fontsize=14, fontweight="bold")
plt.xlabel('Grid Size', fontsize=14, fontweight="bold")
plt.title('Sum utility - Grid Size')
plt.legend(prop={'size': 14})
plt.show(block=False)
address = '/data/'
plt.savefig(address + 'Max Util_Grid.pdf', bbox_inches='tight')

#pass
