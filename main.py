#########################################################
# import libraries
from config import Size, Config_Dim as Dim, Config_General as General, Config_Param as Param, Config_Power as Power, Config_Path
import location_gen as loc
import csi as csi_module
import numpy as np
import util_primary as u_p
import util_fusion as u_f
import jain_index as jain_func
from gain_util_jain import reward_val
import matplotlib.pyplot as plt
from statefromloc import getstateloc
from action_sel import action_explore, action_exploit
from csi import get_csi
from findq import find_max_q_next
from copy import deepcopy
from random import seed
import time


SEED = 0
np.random.seed(SEED)
seed(a=SEED)
# seed(a=None)


#########################################################
# General Flags
Flag_Print = False

#########################################################
# Scenario Definition
print(General, "Size = ", Size)
num_UAV = General.get('NUM_UAV')
num_Eps = General.get('NUM_EPS')
num_Step = General.get('NUM_STEP')
num_Pkt = General.get('NUM_PKT')
num_Run = General.get('NUM_RUN')

pathDist = Config_Path.get('PathDist')
pathH = Config_Path.get('PathH')

location_init = loc.location(num_UAV,
                             Dim.get('Height'), Dim.get('Length'), Dim.get('Width'),
                             Dim.get('UAV_L_MAX'), Dim.get('UAV_L_MIN'),
                             Dim.get('UAV_W_MAX'), Dim.get('UAV_W_MIN'), pathDist,
                             General.get('Location_SaveFile'), General.get('PlotLocation'), Dim.get('Divider'))

loc_dict = location_init
Length = Dim.get('Length')
Width = Dim.get('Width')
Divider = Dim.get('Divider')

CSI_Param = csi_module.load_csi(num_UAV, loc_dict, pathH, General.get('CSI_SaveFile'))

gamma = 0.3
alpha = 0.1
epsilon = 0.1
const_greedy = 0.9

#########################################################
# Initialization
for Run in range(0, num_Run):
    u_primary = np.zeros([num_Step, num_Eps])
    u_fusion = np.zeros([num_Step, num_Eps])
    sum_utility = np.zeros([num_Step, num_Eps])

    reward = np.zeros([num_Step, num_Eps])
    delta_upn = np.zeros([num_Step, num_Eps])
    delta_ufn = np.zeros([num_Step, num_Eps])
    delta_up = np.zeros([num_Step, num_Eps])
    delta_un = np.zeros([num_Step, num_Eps])

    num_F = np.zeros([num_Step, num_Eps], dtype=int)
    num_R = np.zeros([num_Step, num_Eps], dtype=int)

    jainVal = np.zeros([num_Step, num_Eps])
    jain_scaled = np.zeros([num_Step, num_Eps])

    #########################################################
    # Initialization for the MA RL algorithm

    Dim_L = Length
    Dim_W = Width
    num_states = Dim_L * Dim_W
    num_action = 6  # 0: Up, 1: down, 2: Left, 3: Right, 4: Fusion, 5: Relay
    action_list = [0, 1, 2, 3, 4, 5]
    grid_states = np.zeros([Dim_L, Dim_W])

    X_Mat = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    Y_Mat = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)

    State_Mat = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    next_state_index = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)

    action = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    
    task_matrix = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    prev_task = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    task_diff = np.zeros([num_Step, num_Eps], dtype=int)
    
    move_matrix = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    prev_move = np.zeros([num_Step, num_Eps, num_UAV], dtype=int)
    move_diff = np.zeros([num_Step, num_Eps], dtype=int)

    #########################################################
    # Main Function of the Simulation

    # qVal = np.zeros([num_states, num_states, num_action, num_action])

    qVal_dim = []
    qVal_dim += [num_states for _ in range(num_UAV)]
    qVal_dim += [num_action for _ in range(num_UAV)]
    qVal = np.zeros(qVal_dim)


    timer = 0
    for Eps in range(0, num_Eps):
        timer = time.perf_counter()
        number_meet = np.zeros(num_UAV * [num_states], dtype=int)
        X_U = loc_dict.get('X_U')
        Y_U = loc_dict.get('Y_U')

        for Step in range(0, num_Step):
            if num_Eps == 1:
                print (" -----------------Epoch = %d,  Step = %d ----------------- " % (Eps, Step))
            X_Mat[Step, Eps, :] = np.squeeze(X_U)
            Y_Mat[Step, Eps, :] = np.squeeze(Y_U)
            state_index = getstateloc(X_U, Y_U, Size)
            exploration_current_state = deepcopy(state_index)
            State_Mat[Step, Eps, :] = np.squeeze(state_index)
            number_meet[state_index[0], state_index[1]] += 1

            if Step > 0:
                prev_task[Step, Eps, :] = task_matrix[Step-1, Eps, :].copy(order='C')
                prev_move[Step, Eps, :] = move_matrix[Step-1, Eps, :].copy(order='C')

            if np.random.rand() < epsilon:
                # Exploration
                perm_UAV_list = np.arange(num_UAV)
                for UAV in np.random.permutation(perm_UAV_list):
                    action[Step, Eps, UAV], X_U[UAV], Y_U[UAV], state_new = action_explore(X_U[UAV], Y_U[UAV], action_list, Size, exploration_current_state, UAV)
                    # State_Mat[Step, Eps, UAV] = state_new[UAV]
                    if action[Step, Eps, UAV] == 4 or action[Step, Eps, UAV] == 5:
                        task_matrix[Step, Eps, UAV] = action[Step, Eps, UAV] - 4
                        move_matrix[Step, Eps, UAV] = move_matrix[Step-1, Eps, UAV]
                    else:
                        if Step > 0:
                            task_matrix[Step, Eps, UAV] = task_matrix[Step-1, Eps, UAV]
                            move_matrix[Step, Eps, UAV] = action[Step, Eps, UAV]  # TODO: check: this is not 0-1 like task_matrix.
                            
            else:
                # Exploitation
                action[Step, Eps, :], X_U, Y_U, state_new = action_exploit(X_U, Y_U, action_list, Size, state_index, qVal)
                for UAV in np.arange(num_UAV):
                    if action[Step, Eps, UAV] == 4 or action[Step, Eps, UAV] == 5:
                        task_matrix[Step, Eps, UAV] = action[Step, Eps, UAV] - 4
                        move_matrix[Step, Eps, UAV] = move_matrix[Step-1, Eps, UAV]
                    else:
                        if Step > 0:
                            task_matrix[Step, Eps, UAV] = task_matrix[Step-1, Eps, UAV]
                            move_matrix[Step, Eps, UAV] = action[Step, Eps, UAV]  # TODO: check: this is not 0-1 like task_matrix.

            task_diff[Step, Eps] = np.sum(np.not_equal(task_matrix[Step, Eps, :], prev_task[Step, Eps, :]))
            move_diff[Step, Eps] = np.sum(np.not_equal(move_matrix[Step, Eps, :], prev_move[Step, Eps, :]))

            if Flag_Print:
                print(" Current State = ", state_index[0], state_index[1])
                print(" Current X = ", X_Mat[Step, Eps, :])
                print(" Current Y = ", Y_Mat[Step, Eps, :])
                print(" Actions = ", action[Step, Eps, 0], action[Step, Eps, 1])
                print(" New State = ", state_new[0], state_new[1])
                print(" New X = ", X_U[0], X_U[1])
                print(" New Y = ", Y_U[0], Y_U[1])
                print(" Tasks = ", task_matrix[Step, Eps, 0], task_matrix[Step, Eps, 1])
            #################################
            # Updating utilities
            csi_coef = get_csi(num_UAV, loc_dict, X_Mat[Step, Eps, :], Y_Mat[Step, Eps, :])
            u_primary[Step, Eps] = u_p.utility(task_matrix[Step, Eps, :], csi_coef, General, Power)
            u_fusion[Step, Eps] = u_f.utility(task_matrix[Step, Eps, :], csi_coef, General, Power)

            uav_r = np.sum(task_matrix[Step, Eps, :])  # 1 = Relay, 0 = Fusion
            uav_r = int(uav_r)
            uav_f = int(General.get('NUM_UAV') - uav_r)
            jainVal[Step, Eps], jain_scaled[Step, Eps] = jain_func.jain(uav_f, uav_r)

            if uav_f == 0 or uav_r == 0:
                u_primary[Step, Eps] = 0
                u_fusion[Step, Eps] = 0
            sum_utility[Step, Eps] = u_primary[Step, Eps] + u_fusion[Step, Eps]

            #################################
            # Updating reward
            if Step == 0:
                reward[Step, Eps], delta_up[Step, Eps], delta_ufn[Step, Eps] = \
                    reward_val(u_primary[Step, Eps], 0, u_fusion[Step, Eps], 0, jain_scaled[Step, Eps], Param, uav_r,
                               uav_f, u_primary[:, Eps], u_fusion[:, Eps], sum_utility[0, Eps])
            else:
                reward[Step, Eps], delta_up[Step, Eps], delta_ufn[Step, Eps] = \
                    reward_val(u_primary[Step, Eps], u_primary[Step-1, Eps], u_fusion[Step, Eps], u_fusion[Step-1, Eps],
                               jain_scaled[Step, Eps], Param, uav_r, uav_f, u_primary[:, Eps], u_fusion[:, Eps],
                               sum_utility[0: Step, Eps])
            if Flag_Print:
                print(" Primary Utility = ", u_primary[Step, Eps])
                print(" UAV Utility = ", u_fusion[Step, Eps])
                print(" SUM Utility = ", sum_utility[Step, Eps])
                print(" # of Relay = ", uav_r, "# of Fusion = ", uav_f)
                print("Reward = ", reward[Step, Eps])

            #################################
            # Updating Q-Table and Q values
            next_state_index[Step, Eps, :] = np.squeeze(getstateloc(X_U, Y_U, Size))
            maxQ_NextState = find_max_q_next(qVal, next_state_index[Step, Eps, :], X_U, Y_U, action_list, Size)

            qVal[state_index[0], state_index[1], action[Step, Eps, 0], action[Step, Eps, 1]] = \
                (1-alpha) * qVal[state_index[0], state_index[1], action[Step, Eps, 0], action[Step, Eps, 1]] + \
                alpha * (reward[Step, Eps] + gamma * maxQ_NextState)

            if Flag_Print:
                print("QVal = ", qVal[state_index[0], state_index[1], action[Step, Eps, 0], action[Step, Eps, 1]])
            # ********************************
            # End of the Each Step

        print (" -------Run = %d ----- Epoch = %d ----------------- Duration = %f " % (Run, Eps, time.perf_counter() - timer))
        # ********************************
        # End of the Each Episode

    if General.get('PlotResult'):
        
        # plt.figure()
        fig, ax1 = plt.subplots()
        color = 'tab:green'
        ax1.set_xlabel('Episodes')
        ax1.set_ylabel('Total and Emergency Throughput', color=color)
        ax1.plot(range(0, num_Eps), np.sum(sum_utility, axis=0), markersize='10', color='blue')
        ax1.plot(range(0, num_Eps), np.mean(u_fusion, axis=1), markersize='10', color='black')
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:cyan'
        ax2.set_ylabel('Primary Throughput', color=color)  # we already handled the x-label with ax1
        ax2.plot(range(0, num_Eps), np.mean(u_primary, axis=1), markersize='10', color='red')
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.grid(True)
        plt.show(block=False)
        plt.savefig('Throughput.png')

        plt.figure()
        plt.plot(range(0, num_Eps), np.mean(task_diff, axis=1), markersize='10', color='red')
        plt.plot(range(0, num_Eps), np.mean(move_diff, axis=1), markersize='10', color='blue')
        plt.grid(True)
        plt.ylabel('Number of Switch-Movement')
        plt.xlabel('Episodes')
        plt.savefig('Number of Switch-Movement.png')
        plt.show(block=False)

        plt.figure()
        plt.plot(range(0, num_Eps), num_Step, markersize='10', color='black')
        plt.grid(True)
        plt.ylabel('Steps')
        plt.xlabel('Episodes')
        plt.savefig('Steps per Episodes.png')
        plt.show(block=False)

    outputFile = '\data\Out_greedy_Size_%d_Run_%d_Eps_%d_Step_%d.npz' % (Size, Run, num_Eps, num_Step)  # Windows

    np.savez(outputFile, u_primary=u_primary, u_fusion=u_fusion, sum_utility=sum_utility, reward=reward, num_F=num_F,
             num_R=num_R, X_Mat=X_Mat, Y_Mat=Y_Mat, State_Mat=State_Mat, action=action, task_matrix=task_matrix,
             next_state_index=next_state_index, task_diff=task_diff, qVal=qVal)
    
    # End of the Each Run

# seed(1)
