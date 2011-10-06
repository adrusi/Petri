from petri import *
from old_version import *
import argparse

parser = argparse.ArgumentParser(description="Simulate the change in population of bacteria")
parser.add_argument("-w", "--wrap", action="store_true", dest="wrap")
parser.add_argument("-s", "--size", type=int, default=50, dest="dim")
parser.add_argument("-e", "--edition", type=int, choices=[1, 2], default=1, dest="version")
parser.add_argument("-d", "--dos", action="store_true", dest="dos")
args = parser.parse_args()

if args.version == 1:
  v_one(args.dos, args.dim)
elif args.version == 2:
  v_two(args.wrap, args.dim)
