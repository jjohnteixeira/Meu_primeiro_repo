import matplotlib.pyplot as plt
from math import atan2, sin, cos, sqrt, pi, degrees

def area(pts):
  'Area of cross-section.'
  
  if pts[0] != pts[-1]:
    pts = pts + pts[:1]
  x = [ c[0] for c in pts ]
  y = [ c[1] for c in pts ]
  s = 0
  for i in range(len(pts) - 1):
    s += x[i]*y[i+1] - x[i+1]*y[i]
  return s/2


def centroid(pts):
  'Location of centroid.'
  
  if pts[0] != pts[-1]:
    pts = pts + pts[:1]
  x = [ c[0] for c in pts ]
  y = [ c[1] for c in pts ]
  sx = sy = 0
  a = area(pts)
  for i in range(len(pts) - 1):
    sx += (x[i] + x[i+1])*(x[i]*y[i+1] - x[i+1]*y[i])
    sy += (y[i] + y[i+1])*(x[i]*y[i+1] - x[i+1]*y[i])
  return sx/(6*a), sy/(6*a)


def inertia(pts):
  'Moments and product of inertia about centroid.'
  
  if pts[0] != pts[-1]:
    pts = pts + pts[:1]
  x = [ c[0] for c in pts ]
  y = [ c[1] for c in pts ]
  sxx = syy = sxy = 0
  a = area(pts)
  cx, cy = centroid(pts)
  for i in range(len(pts) - 1):
    sxx += (y[i]**2 + y[i]*y[i+1] + y[i+1]**2)*(x[i]*y[i+1] - x[i+1]*y[i])
    syy += (x[i]**2 + x[i]*x[i+1] + x[i+1]**2)*(x[i]*y[i+1] - x[i+1]*y[i])
    sxy += (x[i]*y[i+1] + 2*x[i]*y[i] + 2*x[i+1]*y[i+1] + x[i+1]*y[i])*(x[i]*y[i+1] - x[i+1]*y[i])
  # return sxx/12 - a*cy**2, syy/12 - a*cx**2, sxy/24 - a*cx*cy
  return sxx/12, syy/12, sxy/24


def principal(Ixx, Iyy, Ixy):
  'Principal moments of inertia and orientation.'
  
  avg = (Ixx + Iyy)/2
  diff = (Ixx - Iyy)/2      # signed
  I1 = avg + sqrt(diff**2 + Ixy**2)
  I2 = avg - sqrt(diff**2 + Ixy**2)
  theta = atan2(-Ixy, diff)/2
  return I1, I2, theta


def summary(pts):
  'Text summary of cross-sectional properties.'
  
  a = area(pts)
  cx, cy = centroid(pts)
  Ixx, Iyy, Ixy = inertia(pts)
  I1, I2, theta = principal(Ixx, Iyy, Ixy)
  summ = """Area
  A = {}
Centroid
  cx = {}
  cy = {}
Moments and product of inertia
  Ixx = {}
  Iyy = {}
  Ixy = {}
Principal moments of inertia and direction
  I1 = {}
  I2 = {}
  θ︎ = {}°""".format(a, cx, cy, Ixx, Iyy, Ixy, I1, I2, degrees(theta))
  return summ

 
def outline(pts, basename='section', format='pdf', size=(8, 8), dpi=100):
  'Draw an outline of the cross-section with centroid and principal axes.'
  
  if pts[0] != pts[-1]:
    pts = pts + pts[:1]
  x = [ c[0] for c in pts ]
  y = [ c[1] for c in pts ]
  
  # Get the bounds of the cross-section
  minx = min(x)
  maxx = max(x)
  miny = min(y)
  maxy = max(y)
  
  # Whitespace border is 5% of the larger dimension
  b = .05*max(maxx - minx, maxy - miny)
  
  # Get the properties needed for the centroid and principal axes
  cx, cy = centroid(pts)
  i = inertia(pts)
  p = principal(*i)
  
  # Principal axes extend 10% of the minimum dimension from the centroid
  length = min(maxx-minx, maxy-miny)/10
  a1x = [cx - length*cos(p[2]), cx + length*cos(p[2])]
  a1y = [cy - length*sin(p[2]), cy + length*sin(p[2])]
  a2x = [cx - length*cos(p[2] + pi/2), cx + length*cos(p[2] + pi/2)]
  a2y = [cy - length*sin(p[2] + pi/2), cy + length*sin(p[2] + pi/2)]
  
  # Plot and save
  # Axis colors chosen from http://mkweb.bcgsc.ca/colorblind/
  fig, ax = plt.subplots(figsize=size)
  ax.plot(x, y, 'k*-', lw=2)
  ax.plot(a1x, a1y, '-', color='#0072B2', lw=2)     # blue
  ax.plot(a2x, a2y, '-', color='#D55E00')           # vermillion
  ax.plot(cx, cy, 'ko', mec='k')
  ax.set_aspect('equal')
  plt.xlim(xmin=minx-b, xmax=maxx+b)
  plt.ylim(ymin=miny-b, ymax=maxy+b)
  filename = basename + '.' + format
  plt.savefig(filename, format=format, dpi=dpi)
  plt.close()

if __name__ == "__main__":
  student = "Fernanda"
  pts = [(0.8071752,1.3929228),
(0.8071752,1.3929228),
(0.8600110,1.3809864),
(0.8667849,1.3579882),
(0.8640753,1.3254607),
(0.8871063,1.3025415),
(0.9020088,1.2673899),
(0.9033635,1.2430107),
(0.8735587,1.2388018),
(0.8708492,1.2184671),
(0.8437538,1.2210451),
(0.8437538,1.2413666),
(0.8058204,1.2533754),
(0.7651775,1.2545328),
(0.7380822,1.2489822),
(0.7136964,1.2231233),
(0.7150511,1.1838417),
(0.7218250,1.1527150),
(0.6987940,1.1471841),
(0.6662796,1.1172214),
(0.6662796,1.0901261),
(0.6811820,1.0874890),
(0.7150511,1.0686867),
(0.7150511,1.0375271),
(0.6974392,1.0198296),
(0.6622153,1.0196586),
(0.6351200,1.0357843),
(0.6147985,1.0343309),
(0.6080247,1.0519099),
(0.5998961,1.0654181),
(0.5998961,1.0830301),
(0.6202176,1.0939668),
(0.6283462,1.1224564),
(0.6486676,1.1401670),
(0.6486676,1.1930028),
(0.6486676,1.2092600),
(0.6269914,1.2294762),
(0.6351200,1.2620301),
(0.6269914,1.2863764),
(0.6567962,1.3068426),
(0.6771177,1.3394556),
(0.6811820,1.3584420),
(0.7015035,1.3666692),
(0.7326631,1.3600467),
(0.7516298,1.3574292),
(0.7854989,1.3616579)]
  
  outline(pts, basename=student)
  print(30*"=")
  print(">>>>", student)
  print(summary(pts))
