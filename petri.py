import random
# from random import *
# from colors import *
import os
import math
import sys
import time
def v_two(wrap, dim, delay, light):

  def gaurd(n):
    if n < 0:
      return dim - 1 if wrap else 1
    elif n > dim - 1:
      return 0 if wrap else dim - 2
    else:
      return n

  def gen_row(min, max):
    return [random.randint(min, max) if random.random() <= 0.4 else 0 for i in range(0, dim)]

  nutrients = [gen_row(0, 5) for i in range(0, dim)]

  class Cell:
    age = 0
    energy = 1
    x = None
    y = None
    tire = 5

    def __init__(self, x, y):
      self.x = x
      self.y = y

    def do_age(self):
      self.age += 1
      if self.age == 10:
        cells[self.x][self.y] = None
        nutrients[self.x][self.y] += int(math.floor(self.energy / 2))
        if nutrients[self.x][self.y] > 5:
          nutrients[self.x][self.y] = 5
        return
      if self.age >= 5 and self.energy >= 4:      
        coords = self.has_space()
        if coords:
          cells[coords[0]][coords[1]] = Cell(coords[0], coords[1])
          self.age = 0
          cells[coords[0]][coords[1]].energy = int(math.ceil(self.energy / 2))
          self.energy = int(math.ceil(self.energy / 2))
      if self.has_nutrition():
        self.eat()
      else:
        self.move_toward_food()
      if self.has_nutrition():
        self.eat()
      if self.tire == 0:
        self.tire = 5
        self.energy -= 1
      else:
        self.tire -= 1
      if self.energy == 0:
        if random > 0.6:
          nutrients[self.x][self.y] += 1
          if nutrients[self.x][self.y] > 5: nutrients[self.x][self.y] = 5 
        cells[self.x][self.y] = None

    def has_nutrition(self):
      return nutrients[self.x][self.y] >= 1

    def eat(self):
      if nutrients[self.x][self.y] > 1:
        ammount = random.randint(1, 2) if random.random() > 0.5 else 1
        nutrients[self.x][self.y] -= ammount
        self.energy += ammount
      else:
        nutrients[self.x][self.y] -= 1
        self.energy += 1

    def move_toward_food(self):
      if self.energy >= 3:
        directions = ["u", "ur", "r", "dr", "d", "dl", "l", "ul"]
        points = [0, 0, 0, 0, 0, 0, 0, 0]
        # random.shuffle(directions)
        for i in range(0, len(directions)):
          direction = directions[i]
          nut = self.nutrition_exists(direction)
          if self.unoccupied(direction) and nut:
            # self.move(direction)
            # self.energy -= 2
            # break
            points[i] = (nut + random.randint(-1, 1)) + (3 - random.randint(0, 2) if self.has_neighbor(direction) else 0)
        num_non_zeros = 0
        for i in points:
          if i != 0: num_non_zeros += 1
        if num_non_zeros == 0: return
        avg = sum(points) / num_non_zeros
        opts = []
        for i in range(0, len(points)):
          if float(points[i]) >= avg:
            opts.append(directions[i])
        random.shuffle(opts)
        choice = opts[0]
        self.move(choice)

    def unoccupied(self, d):
      map = {
          "u": (0, -1),
          "ur": (1, -1),
          "r": (1, 0),
          "dr": (1, 1),
          "d": (0, 1),
          "dl": (-1, 1),
          "l": (-1, 0),
          "ul": (-1, -1)
      }
      directions = ["u", "ur", "r", "dr", "d", "dl", "l", "ul"]
      random.shuffle(directions)
      for direction in directions:
        diff = map[direction]
        x = self.x + diff[0]
        y = self.y + diff[1]
        if wrap:
          if x == -1: x = dim - 1
          if x == dim: x = 0
          if y == -1: y = dim - 1
          if y == dim: y = 0
        else:
          if x == -1: x = 1
          if x == dim: x = dim - 2
          if y == -1: y = 1
          if y == dim: y = dim - 2
        return cells[x][y] == None

    def has_space(self):
      map = {
          "u": (0, -1),
          "ur": (1, -1),
          "r": (1, 0),
          "dr": (1, 1),
          "d": (0, 1),
          "dl": (-1, 1),
          "l": (-1, 0),
          "ul": (-1, -1)
      }
      directions = ["u", "ur", "r", "dr", "d", "dl", "l", "ul"]
      random.shuffle(directions)
      for direction in directions:
        if self.unoccupied(direction):
          diff = map[direction]
          x = self.x + diff[0]
          y = self.y + diff[1]
          if wrap:
            if x == -1: x = dim - 1
            if x == dim: x = 0
            if y == -1: y = dim - 1
            if y == dim: y = 0
          else:
            if x == -1: x = 1
            if x == dim: x = dim - 2
            if y == -1: y = 1
            if y == dim: y = dim - 2
          return (x, y)
      return False

    def move(self, d):
      map = {
          "u": (0, -1),
          "ur": (1, -1),
          "r": (1, 0),
          "dr": (1, 1),
          "d": (0, 1),
          "dl": (-1, 1),
          "l": (-1, 0),
          "ul": (-1, -1)
      }
      diff = map[d]
      x = self.x + diff[0]
      y = self.y + diff[1]
      if wrap:
        if x == -1: x = dim - 1
        if x == dim: x = 0
        if y == -1: y = dim - 1
        if y == dim: y = 0
      else:
        if x == -1: x = 1
        if x == dim: x = dim - 2
        if y == -1: y = 1
        if y == dim: y = dim - 2
      cells[x][y] = self
      cells[self.x][self.y] = None
      self.x = x
      self.y = y
      self.energy -= 2

    def nutrition_exists(self, d):
      map = {
          "u": (0, -1),
          "ur": (1, -1),
          "r": (1, 0),
          "dr": (1, 1),
          "d": (0, 1),
          "dl": (-1, 1),
          "l": (-1, 0),
          "ul": (-1, -1)
      }
      diff = map[d]
      x = self.x + diff[0]
      y = self.y + diff[1]
      if wrap:
        if x == -1: x = dim - 1
        if x == dim: x = 0
        if y == -1: y = dim - 1
        if y == dim: y = 0
      else:
        if x == -1: x = 1
        if x == dim: x = dim - 2
        if y == -1: y = 1
        if y == dim: y = dim - 2
      return nutrients[x][y]

    def has_neighbor(self, d):
      map = {
          "u": (0, -1),
          "ur": (1, -1),
          "r": (1, 0),
          "dr": (1, 1),
          "d": (0, 1),
          "dl": (-1, 1),
          "l": (-1, 0),
          "ul": (-1, -1)
      }
      diff = map[d]
      x = self.x + diff[0]
      y = self.y + diff[1]
      if wrap:
        if x == -1: x = dim - 1
        if x == dim: x = 0
        if y == -1: y = dim - 1
        if y == dim: y = 0
      else:
        if x == -1: x = 1
        if x == dim: x = dim - 2
        if y == -1: y = 1
        if y == dim: y = dim - 2
      return cells[gaurd(x)][gaurd(y - 1)] != None or \
             cells[gaurd(x + 1)][gaurd(y - 1)] != None or \
             cells[gaurd(x + 1)][gaurd(y)] != None or \
             cells[gaurd(x + 1)][gaurd(y + 1)] != None or \
             cells[gaurd(x)][gaurd(y + 1)] != None or \
             cells[gaurd(x - 1)][gaurd(y + 1)] != None or \
             cells[gaurd(x - 1)][gaurd(y)] != None or \
             cells[gaurd(x - 1)][gaurd(y - 1)] != None



  cells = []

  for i in range(0, dim):
    row = []
    for j in range(0, dim):
      if random.randint(0, 15) == 15:
        row.append(Cell(i, j))
      else:
        row.append(None)
    cells.append(row)

  def escape_code(nutrition, cell):
    background = []
    if not hasattr(cell, "energy"):
      if not light: background = [255, 251, 246, 242, 237, 232][int(nutrition)]
      else: background = [255, 253, 251, 249, 247, 245][int(nutrition)]
    else:
      n = int(round(cell.energy / 2))
      background = [52, 88, 124, 160, 196, 87][n] if n <= 5 else 5
    return "\033[48;5;%dm \033[0m" % background

  def draw_dish():
    str = "\033[2j"
    for i in range(0, dim):
      for j in range(0, dim):
        str += escape_code(nutrients[i][j], cells[i][j])
      str += "\n"
    return str

  def progress():
    for i in cells:
      for j in i:
        if hasattr(j, "age"):
          j.do_age()
    for i in range(0, dim):
      for j in range(0, dim):
        nutrients[i][j] += random.randint(1, 2) if random.random() > 0.97 else 0
        if nutrients[i][j] > 5: nutrients[i][j] = 5

# os.system("clear")
# print draw_dish()
# progress()
# print "\n"
# print draw_dish()
  os.system("clear")
  print "\033[s",
  while True:
    # os.system("clear")
    # print "\033[2J"
    print "\033[u%s" % draw_dish(),
    progress()
    # foo = raw_input()
    # if foo == "stop": break
    # time.sleep(0.5)
    time.sleep(delay)

  os.system("clear")
