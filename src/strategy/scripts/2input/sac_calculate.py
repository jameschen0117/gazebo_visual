import rospy
from transfer.msg import PPoint
from nubot_common.msg import OminiVisionInfo
import numpy as np
import math 
# Normalization
HALF_MAX_DIS = 900 #cm
FULL_MAX_DIS = 1800 #cm

state = []
HowEnd = 0
input_list = []
pos = []

def callback(data):
    global pos
    pos=[data.robotinfo[0].pos.x, data.robotinfo[0].pos.y, data.robotinfo[0].heading.theta,
        data.obstacleinfo.pos[0].x, data.obstacleinfo.pos[0].y]

def input2state(data):
    global HowEnd
    global pos
    global input_list
    input_list = [0,0,0,0,0,  
                    HowEnd]
    input_list[0:5] = pos
    # print(input_list)
    global state
    state = [0,0,0,0,0,
                    HowEnd]
    state[0]=input_list[0]/100
    state[1]=input_list[1]/100
    state[2]=input_list[2]/math.pi
    state[3]=input_list[3]/100
    state[4]=input_list[4]/100

rospy.Subscriber("/nubot1/omnivision/OmniVisionInfo/GoalInfo", PPoint, input2state)
rospy.Subscriber("/nubot1/omnivision/OmniVisionInfo", OminiVisionInfo, callback)

class sac_calculate():
    def __init__(self):
        pass
    
    def input(self,a):
        global state
        global input_list
        global HowEnd
        # print(a)
        state[5] = a
        # print('s', np.around((input_list), decimals=1 ))
        print('s',['a_x  a_y  ath  b_x  b_y end'])
        print('s', np.around((state), decimals=1 ))
        return state
    def output(self, action):
        action2robot = action[0] * 180
        # print(action2robot) 
        return action2robot
    def reward(self,t):   
        a = 2 #3 #j #2 # 1 kick / avg = 5 kicks i wish
        b = 1 #1 #i #0.5 # goal
        c = 1 #1 #i #0.5 # start
        d = 3 #2 #k #0.3 # opp
        e = 50 # in 5
        f = -10 # out -4
        g = -5 # steal or fly
        # print(reward)
        reward = a *(t[0]/5)+ b *(t[1]/FULL_MAX_DIS)+ c *((FULL_MAX_DIS-t[2])/FULL_MAX_DIS)+ d*(t[3]/HALF_MAX_DIS) +e*t[4] + f*t[5] + g*t[6]
        # reward = 10 * t[0] + 0.5 * t[1] + 10000 * (1/t[2])
        # reward = 8
        return reward



# def action():
# def action2output(action):
    # pass
    # kickpwr 



# if __name__ == '__main__':
#     get_input()


# '''calculate'''

    


# ''' [] about input ''' 



# ''' [] about output '''



# ''' [] about reward '''



# done
