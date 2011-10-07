from petri import *
from old_version import *
import argparse

parser = argparse.ArgumentParser(description="Simulate the change in population of bacteria")
parser.add_argument("-w", "--wrap", action="store_true", default=False, dest="wrap", help="Bacteria that overflow the edges will appear on the opposite side")
parser.add_argument("-l", "--light", action="store_true", default=False, dest="light", help="food will be colored lighter")
parser.add_argument("-s", "--size", type=int, default=50, dest="dim", help="Change the number of squares on the board (number = 1 side length)")
parser.add_argument("-t", "--delay", type=float, default=0.1, dest="speed", help="Change the delay between iterations")
parser.add_argument("-e", "--edition", type=int, choices=[1, 2], default=1, dest="version", help="Choose which version to use")
parser.add_argument("-d", "--dos", action="store_true", dest="dos")
args = parser.parse_args()

if args.version == 1:
  v_one(args.dos, args.dim, args.speed, args.light)
elif args.version == 2:
  v_two(args.wrap, args.dim, args.speed, args.light)
