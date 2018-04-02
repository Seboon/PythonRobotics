"""

Hybrid A* path planning

author: Atsushi Sakai (@Atsushi_twi)

"""

import sys
sys.path.append("../ReedsSheppPath/")

import math
import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt
import reeds_shepp_path_planning as rs

EXTEND_AREA = 5.0  # [m]

show_animation = True


class KDTree:
    """
    Nearest neighbor search class with KDTree
    """

    def __init__(self, data):
        # store kd-tree
        self.tree = scipy.spatial.cKDTree(data)

    def search(self, inp, k=1):
        """
        Search NN
        inp: input data, single frame or multi frame
        """

        if len(inp.shape) >= 2:  # multi input
            index = []
            dist = []

            for i in inp.T:
                idist, iindex = self.tree.query(i, k=k)
                index.append(iindex)
                dist.append(idist)

            return index, dist
        else:
            dist, index = self.tree.query(inp, k=k)
            return index, dist

    def search_in_distance(self, inp, r):
        """
        find points with in a distance r
        """

        index = self.tree.query_ball_point(inp, r)
        return index


class Config:

    def __init__(self, ox, oy, xyreso, yawreso):
        min_x_m = min(ox) - EXTEND_AREA
        min_y_m = min(oy) - EXTEND_AREA
        max_x_m = max(ox) + EXTEND_AREA
        max_y_m = max(oy) + EXTEND_AREA

        ox.append(min_x_m)
        oy.append(min_y_m)
        ox.append(max_x_m)
        oy.append(max_y_m)

        self.minx = int(min_x_m / xyreso)
        self.miny = int(min_y_m / xyreso)
        self.maxx = int(max_x_m / xyreso)
        self.maxy = int(max_y_m / xyreso)

        self.xw = int(self.maxx - self.minx)
        self.yw = int(self.maxy - self.miny)

        self.minyaw = int(- math.pi / yawreso) - 1
        self.maxyaw = int(math.pi / yawreso)
        self.yaww = int(self.maxyaw - self.minyaw)


def hybrid_a_star_planning(start, goal, ox, oy, xyreso, yawreso):
    """
    start
    goal
    ox: x position list of Obstacles [m]
    oy: y position list of Obstacles [m]
    xyreso: grid resolution [m]
    yawreso: yaw angle resolution [rad]
    """

    start[2], goal[2] = rs.pi_2_pi(start[2]), rs.pi_2_pi(goal[2])
    tox, toy = ox[:], oy[:]

    obkdtree = KDTree(np.vstack((tox, toy)).T)

    c = Config(tox, toy, xyreso, yawreso)

    rx, ry, ryaw = [], [], []

    return rx, ry, ryaw


def main():
    print("Start rrt start planning")
    # ====Search Path with RRT====

    ox, oy = [], []

    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(40):
        ox.append(20.0)
        oy.append(i)
    for i in range(40):
        ox.append(40.0)
        oy.append(60.0 - i)

    # Set Initial parameters
    start = [10.0, 10.0, math.radians(90.0)]
    goal = [50.0, 50.0, math.radians(-90.0)]

    xyreso = 2.0
    yawreso = math.radians(15.0)

    rx, ry, ryaw = hybrid_a_star_planning(
        start, goal, ox, oy, xyreso, yawreso)

    plt.plot(ox, oy, ".k")
    rs.plot_arrow(start[0], start[1], start[2])
    rs.plot_arrow(goal[0], goal[1], goal[2])

    plt.grid(True)
    plt.axis("equal")
    plt.show()

    print(__file__ + " start!!")


if __name__ == '__main__':
    main()