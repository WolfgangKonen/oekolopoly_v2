"""
    Test that ``get_boxes.py`` and ``get_boxes2.py`` deliver the same numeric values.

    Measure the execution time of a specific (variable ``tk``) ``get_box*`` method in both versions.
"""
from time import perf_counter
import oekolopoly.oekolopoly.envs.get_boxes as gb
from oekolopoly.oekolopoly.envs.oeko_env import OekoEnv
from oekolopoly.oekolopoly.envs.get_boxes2 import GetBoxes as gb2

# x_code[i]: the sector code for the x-axis sector of diagram i:
# i =      0              5             10             15             20
#                                                       A  B  C  D  V  W
x_code = [-1, 0, 0, 1, 1, 5, 5, 2, 2, 2, 3, 3, 3, 4, 6, 6, 7, 1, 3, 1, 6]
# ptitle[i]: the plot title of diagram i AND the suffix for get_box*:
# i =       0                       5
ptitle = [ "",  "1", "2", "3", "4", "5", "6", "7", "8", "9",
          "10","11","12","13","14", "A", "B", "C", "D", "V", "W"]
o_env = OekoEnv()

if __name__ == "__main__":
    e = 99  # dummy value for extra_points (case k==9)
    for k in range(1, 20+1):
        gb_str = f"get_box{ptitle[k]}"
        vmin = o_env.Vmin[x_code[k]]
        vmax = o_env.Vmax[x_code[k]]
        for i in range(vmin,vmax+1):
            suffix = ", e" if k == 9 else ""
            z1 = f"gb.{gb_str}({i}{suffix})"
            z2 = f"gb2.{gb_str}({i}{suffix})"
            assert eval(z1) == eval(z2), f"Wrong value for k={k}, i={i}"

    tk = 4
    if tk == 1:
        t_start = perf_counter()
        for i in range(100000):         # do not use eval(...) here,
            gb.get_box1(29)             # this would spoil the time measurement
        print(f"Old  gb.get_box1:", perf_counter() - t_start)

        t_start = perf_counter()
        for i in range(100000):
            gb2.get_box1(29)
        print(f"New gb2.get_box1:", perf_counter() - t_start)  # gb2.get_box1(29) is 3 times (!) faster
    elif tk == 2:
        t_start = perf_counter()
        for i in range(100000):         # do not use eval(...) here,
            gb.get_box2(29)             # this would spoil the time measurement
        print(f"Old  gb.get_box2:", perf_counter() - t_start)

        t_start = perf_counter()
        for i in range(100000):
            gb2.get_box2(29)
        print(f"New gb2.get_box2:", perf_counter() - t_start)   # gb2.get_box2(29) is 2 times faster
    elif tk == 4:
        t_start = perf_counter()
        for i in range(100000):         # do not use eval(...) here,
            gb.get_box4(29)             # this would spoil the time measurement
        print(f"Old  gb.get_box4:", perf_counter() - t_start)

        t_start = perf_counter()
        for i in range(100000):
            gb2.get_box4(29)
        print(f"New gb2.get_box4:", perf_counter() - t_start)  # gb2.get_box4(29) is 4 times (!) faster
