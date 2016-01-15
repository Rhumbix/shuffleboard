import matplotlib.path as mplPath
import numpy as np
import yaml

def reverse_list(l):
  return l[::-1]

def param_to_line(l):
  return [l['left']['x'], l['left']['y']], [l['right']['x'], l['right']['y']]

def in_polygon(point, polygon):
  bbPath = mplPath.Path(np.array(polygon))
  return bbPath.contains_point(point)

def score(params, blues, reds):
  endzone_at_top = params['endzone_at_top'] == 'y'
  lines = [ param_to_line(l) for l in params['lines'] ]

  whole_zone = lines[0] + reverse_list(lines[3])
  import pdb; pdb.set_trace()
  reds = [p for p in reds if in_polygon(p, whole_zone)]
  blues = [p for p in blues if in_polygon(p, whole_zone)]

  if endzone_at_top:
    min_reds = min([p[1] for p in reds]) if reds else float('inf')
    min_blues = min([p[1] for p in blues]) if blues else float('inf')
    winner = 'red' if min_reds < min_blues else 'blue'
    if winner == 'red':
      pucks = [p for p in reds if p[1] < min_blues]
    else:
      pucks = [p for p in blues if p[1] < min_reds]

  else:
    max_reds = max([p[1] for p in reds]) if reds else 0
    max_blues = max([p[1] for p in blues]) if blues else 0
    winner = 'red' if max_reds > max_blues else 'blue'
    if winner == 'red':
      pucks = [p for p in reds if p[1] > max_blues]
    else:
      pucks = [p for p in blues if p[1] > max_reds]

  points = 0
  if endzone_at_top:
    zone_3_points = lines[0] + reverse_list(lines[1])
    zone_2_points = lines[1] + reverse_list(lines[2])
    zone_1_points = lines[2] + reverse_list(lines[3])
  else:
    zone_1_points = lines[0] + reverse_list(lines[1])
    zone_2_points = lines[1] + reverse_list(lines[2])
    zone_3_points = lines[2] + reverse_list(lines[3])

  points += len([p for p in pucks if in_polygon(p, zone_1_points)])
  points += len([p for p in pucks if in_polygon(p, zone_2_points)]) * 2
  points += len([p for p in pucks if in_polygon(p, zone_3_points)]) * 3

  return (winner, points)

if __name__ == "__main__":
  open('cheatsheet.yaml', 'r') as f:
    params = yaml.load(f)
    print score(params['wall'], [[13, 14]], [[5,30]])
