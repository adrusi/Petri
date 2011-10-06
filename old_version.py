from random import *
# from colors import *
import os
import math
import sys
import time
def v_one(dos, dim):
  def gen_row(min, max):
    return [randint(min, max) if random() <= 0.4 else 0 for i in range(0, dim)]

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
        cells[self.x][self.y] = None

    def has_nutrition(self):
      return nutrients[self.x][self.y] >= 1

    def eat(self):
      if nutrients[self.x][self.y] > 1:
        ammount = randint(1, 2)
        nutrients[self.x][self.y] -= ammount
        self.energy += ammount
      else:
        nutrients[self.x][self.y] -= 1
        self.energy += 1

    def move_toward_food(self):
      if self.energy >= 3:
        self.energy -= 2
        if self.unoccupied("u") and self.nutrition_exists("u"):
          self.move("u")
        elif self.unoccupied("ur") and self.nutrition_exists("ur"):
          self.move("ur")
        elif self.unoccupied("r") and self.nutrition_exists("r"):
          self.move("r")
        elif self.unoccupied("dr") and self.nutrition_exists("dr"):
          self.move("dr")
        elif self.unoccupied("d") and self.nutrition_exists("d"):
          self.move("d")
        elif self.unoccupied("dl") and self.nutrition_exists("dl"):
          self.move("dl")
        elif self.unoccupied("l") and self.nutrition_exists("l"):
          self.move("l")
        elif self.unoccupied("ul") and self.nutrition_exists("ul"):
          self.move("ul")
        else:
          self.energy += 2

    def unoccupied(self, d):
      if d == "u":
        return self.y - 1 >= 0 and cells[self.x][self.y - 1] == None
      elif d == "ur":
        return self.x + 1 < dim and self.y - 1 >= 0 and cells[self.x + 1][self.y - 1] == None
      elif d == "r":
        return self.x + 1 < dim and cells[self.x + 1][self.y] == None
      elif d == "dr":
        return self.x + 1 < dim and self.y + 1 < dim and cells[self.x + 1][self.y + 1] == None
      elif d == "d":
        return self.y + 1 < dim and cells[self.x][self.y + 1] == None
      elif d == "dl":
        return self.x - 1 >= 0 and self.y + 1 < dim and cells[self.x - 1][self.y + 1] == None
      elif d == "l":
        return self.x - 1 >= 0 and cells[self.x - 1][self.y] == None
      elif d == "ul":
        return self.x - 1 >= 0 and self.y - 1 >= 0 and cells[self.x - 1][self.y - 1] == None
      else:
        return False

    def has_space(self):
      if self.unoccupied("u"): return (self.x, self.y - 1)
      elif self.unoccupied("ur"): return (self.x + 1, self.y - 1)
      elif self.unoccupied("r"): return (self.x + 1, self.y)
      elif self.unoccupied("dr"): return (self.x + 1, self.y + 1)
      elif self.unoccupied("d"): return (self.x, self.y + 1)
      elif self.unoccupied("dl"): return (self.x - 1, self.y + 1)
      elif self.unoccupied("l"): return (self.x - 1, self.y)
      elif self.unoccupied("ul"): return (self.x - 1, self.y - 1)
      else: return False

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
      cells[self.x + diff[0]][self.y + diff[1]] = self
      cells[self.x][self.y] = None
      self.x = self.x + diff[0]
      self.y = self.y + diff[1]

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
      return nutrients[self.x + diff[0]][self.y + diff[1]]



  cells = []

  for i in range(0, dim):
    row = []
    for j in range(0, dim):
      if randint(0, 15) == 15:
        row.append(Cell(i, j))
      else:
        row.append(None)
    cells.append(row)

  def escape_code(nutrition, cell):
    if dos:
      background = ["F", "7", "E", "6", "8", "0"][int(nutrition)]
      text = int(round(cell.energy / 2)) if hasattr(cell, "energy") else " "
      foreground = "4"
      os.system("color %s%s" % (background, foreground))
      return str(text)
    else:
      background = [255, 250, 245, 240, 235, 232][int(nutrition)]
      text = int(round(cell.energy / 2)) if hasattr(cell, "energy") else " "
      foreground = 196
      return "\033[48;5;%dm\033[38;5;%dm%s\033[0m" % (background, foreground, text)

  def draw_dish():
    str = ""
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
        nutrients[i][j] += randint(1, 2) if random() > 0.97 else 0
        if nutrients[i][j] > 5: nutrients[i][j] = 5

  os.system("clear")
# print draw_dish()
# progress()
# print "\n"
# print draw_dish()
  print "\033[s",
  while True:
    # os.system("clear")
    print "\033[u%s" % draw_dish()
    progress()
    # foo = raw_input()
    # if foo == "stop": break
    time.sleep(0.1)
