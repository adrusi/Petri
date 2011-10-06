def escape_code(nutrition, cell):
  background = [255, 250, 245, 240, 235, 232][int(nutrition)]
  text = int(round(cell.energy / 3)) if hasattr(cell, "energy") else " "
  foreground = 196
  return "\033[48;5;%dm\033[38;5;%dm%s\033[0m" % (background, foreground, text)
