from strategy_ddpg import *
# from GA_strategy import *


if __name__ == '__main__':
    strategy = Strategy('A')
    strategy.ros_init()
    strategy.workA()