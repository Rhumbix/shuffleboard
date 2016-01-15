import matplotlib.path as mplPath
import numpy as np
import yaml
import cv2
import sys
import shuffle_cv

with open('cheatsheet.yaml', 'r') as f:
  params = yaml.load(f)
  endzone_at_top = params['endzone_at_top'] == 'y'

def reverse_list(l):
  return l[::-1]

def param_to_line(l):
  return [l['left']['x'], l['left']['y']], [l['right']['x'], l['right']['y']]

def in_polygon(point, polygon):
  bbPath = mplPath.Path(np.array(polygon))
  return bbPath.contains_point(point)

def points_for_pucks(pucks, lines):
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
  return points

def score(blues, reds):
  lines = [ param_to_line(l) for l in params['lines'] ]

  whole_zone = lines[0] + reverse_list(lines[3])
  reds = [p for p in reds if in_polygon(p, whole_zone)]
  blues = [p for p in blues if in_polygon(p, whole_zone)]

  if endzone_at_top:
    min_reds = min([p[1] for p in reds]) if reds else float('inf')
    min_blues = min([p[1] for p in blues]) if blues else float('inf')
    winner = 'red' if min_reds < min_blues else 'blue'
    if winner == 'red':
      red_pucks = [p for p in reds if p[1] < min_blues]
      return {'red': points_for_pucks(red_pucks, lines), 'blue': 0}
    else:
      blue_pucks = [p for p in blues if p[1] < min_reds]
      return {'red': 0, 'blue': points_for_pucks(blue_pucks, lines)}

  else:
    max_reds = max([p[1] for p in reds]) if reds else 0
    max_blues = max([p[1] for p in blues]) if blues else 0
    winner = 'red' if max_reds > max_blues else 'blue'
    if winner == 'red':
      red_pucks = [p for p in reds if p[1] > max_blues]
      return {'red': points_for_pucks(red_pucks, lines), 'blue': 0}
    else:
      blue_pucks = [p for p in blues if p[1] > max_reds]
      return {'red': 0, 'blue': points_for_pucks(blue_pucks, lines)}

def get_score(image_file):
  shuffle_cv.mask_for_blue(image_file)
  shuffle_cv.mask_for_red(image_file)
  blue_pucks = shuffle_cv.find_pucks('static/img/blue.jpg')
  red_pucks = shuffle_cv.find_pucks('static/img/red.jpg')
  return score(blue_pucks, red_pucks)

if __name__ == "__main__":
  print get_score(sys.argv[1])
