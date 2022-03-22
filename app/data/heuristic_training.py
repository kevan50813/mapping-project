#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


import sqlite3
import json
from pygeodesy.sphericalNvector import LatLon, Nvector
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
import multiprocessing

# In[3]:


# load in the sqlite file into memory

db_file= "scan_data.sqlite"

# basic setup
con = sqlite3.connect(db_file)
con.row_factory = sqlite3.Row
cur = con.cursor()

# join on the ID, as the base geometry BLOB in the ScanData table is raw binary
# we could convert that to geomtry via a QGIS package for JSON, but joining works just as well
db_rows = con.execute(
    "SELECT ScanData.pkuid, ScanData.data, ScanData.level, \
    idx_ScanData_geometry.xmin, idx_ScanData_geometry.xmax, idx_ScanData_geometry.ymin, idx_ScanData_geometry.ymax \
    FROM ScanData \
    INNER JOIN idx_ScanData_geometry \
    ON ScanData.pkuid=idx_ScanData_geometry.pkid"
)
# turn it into our favourite thing ever, a dictionary :)
db_dict = [dict(row) for row in db_rows]
print(f"Obtained {len(db_dict)} rows from database.")

# ensure the connection is closed
con.close()


# In[4]:


# load in the AP locational data for referencing

# we dont care about the preamble, so just get the features
with open("heuristic_nodes.json", 'r') as f:
    node_data = json.load(f)['features']
    
# will hold the AP locational data for referencing later
node_dict = {}

# set up dictionary with the MAC as the key, and the level and coordinates as values
for entry in node_data:
    data = entry['properties']
    
    # only take Points with a MAC value, i.e. only take APs
    if not data['mac_addres'] is None:
        
        # skim off the last char of the key. still unique. this makes later processing O(1) instead of O(n)
        node_dict[data['mac_addres'][:-1]] = {
            "level": int(data['level']),
            "coordinates": entry['geometry']['coordinates']
        }

# sort based on level
node_dict = dict(sorted(node_dict.items(), key=lambda x:x[1]['level']))        

for mac, data in node_dict.items():
    print(f"MAC {mac} on Level {data['level']} := {data['coordinates']}")


# In[5]:


def compare_networks(data, level):
    
    common_list = []
    
    for scan in data:
        common_scan = []

        for network in scan:
            mac = network['BSSID'][:-1]
            
            # get networks of known location on the same floor
            try:
                entry = node_dict[mac]
                if entry['level'] == level:
                    
                    # ensure the AP hasnt already been added from a similar MAC but same location
                    # same location will break trilateration entirely
                    if not any(net for net in common_scan if net["BSSID"][:-1] == mac):
                        pos = LatLon(entry['coordinates'][0], entry['coordinates'][1])
                        network['coordinates'] = pos
                        del network["SSID"]
                        common_scan.append(network)
            except Exception:
                ...
        
        common_list.append(common_scan)
            
    return common_list


# In[6]:


# turn sqlite file into dictionary, referencing scan data against AP dict to add locations

# the end dict that will hold all data for trilateration
ap_dict = {}

for row in db_dict:
    
    # point is a circle defined by bounding box - get center
    x = (row['xmin'] + row['xmax']) / 2
    y = (row['ymin'] + row['ymax']) / 2
    
    # main key for this dict will be by floor
    level = row['level']
    if not level in ap_dict:
        ap_dict[level] = {}
    
    # augment scan data with positional data for each scanned AP
    ap_dict[level][(x, y)] = compare_networks(json.loads(row['data']), level)
    
# sort based on floor, and display end message
ap_dict = dict(sorted(ap_dict.items()))
print(f"Dict created, with {len(ap_dict)} keys with the following value lengths: {[len(val) for val in ap_dict.values()]}\n")

#for level, level_data in ap_dict.items():
#    print(f"Level {level}")
#    for geometry, scan in level_data.items():
#        print(f"{geometry} := net count/scan: {[len(s) for s in scan]}")


# In[14]:


# copy paste of the EXACT trilateration algo used in jsgeodesy
# the python implementation is different! so we use this one

point_nvectors = {}

#@jit(nopython=True)
def trilaterate(point1, distance1, point2, distance2, point3, distance3, radius=6371e3):
        # from en.wikipedia.org/wiki/Trilateration
        
        #'''
        try:
            n1 = point_nvectors[(point1.lat, point1.lon)]
        except KeyError:
            n1 = point1.toNvector()
            point_nvectors[(point1.lat, point1.lon)] = n1
        
        try:
            n2 = point_nvectors[(point2.lat, point2.lon)]
        except KeyError:
            n2 = point2.toNvector()
            point_nvectors[(point2.lat, point2.lon)] = n2
        
        try:
            n3 = point_nvectors[(point3.lat, point3.lon)]
        except KeyError:
            n3 = point3.toNvector()
            point_nvectors[(point3.lat, point3.lon)] = n3
        #'''
        
        '''
        n1 = point1.toNvector()
        n2 = point2.toNvector()
        n3 = point3.toNvector()
        '''
        δ1 = float(distance1)/float(radius)
        δ2 = float(distance2)/float(radius)
        δ3 = float(distance3)/float(radius)

        # the following uses x,y coordinate system with origin at n1, x axis n1->n2
        eX = n2.minus(n1).unit()                         # unit vector in x direction n1->n2
        i = eX.dot(n3.minus(n1))                         # signed magnitude of x component of n1->n3
        eY = n3.minus(n1).minus(eX.times(i)).unit()      # unit vector in y direction
        d = n2.minus(n1).length                          # distance n1->n2
        j = eY.dot(n3.minus(n1))                         # signed magnitude of y component of n1->n3
        x = (δ1*δ1 - δ2*δ2 + d*d) / (2*d)                # x component of n1 -> intersection
        y = (δ1*δ1 - δ3*δ3 + i*i + j*j) / (2*j) - x*i/j  # y component of n1 -> intersection
        # const eZ = eX.cross(eY);                            # unit vector perpendicular to plane
        # const z = Math.sqrt(δ1*δ1 - x*x - y*y);             # z will be NaN for no intersections

        n = n1.plus(eX.times(x)).plus(eY.times(y)) # note don't use z component; assume points at same height

        return Nvector(n.x, n.y, n.z).toLatLon()


# In[15]:


# the formula we're tuning!
# rssiToDistance in Trilateration.js
def rssi_to_distance(A, n, RSSI):
    dist = math.pow(10, ((RSSI - A) / (-10 * n)))
    return dist

# trilaterate in Trilateration.js
def do_trilaterate(A, n, triplet):
    
    #points = [LatLon(net['coordinates'][0], net['coordinates'][1]) for net in triplet]
    points = [net['coordinates'] for net in triplet]
    distances = [rssi_to_distance(A, n, net['RSSI']) for net in triplet]
    
    try:
        point = trilaterate(
            points[0],
            distances[0],
            points[1],
            distances[1],
            points[2],
            distances[2]
        )
        
        pointArr = [point.lat, point.lon]
    
    except Exception as e:
        print(e)
        pointArr = [-1, -1]
        
    return pointArr

# distance in Trilateration.js
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# getStats in Trilateration.js
def get_stats(data):
    pointSum = [sum(i) for i in zip(*data)]
    
    avg = [pointSum[0] / len(data), pointSum[1] / len(data)]
    sumErrSq = sum([distance(point, avg) ** 2 for point in data])
    
    variance = sumErrSq / len(data)
    sd = math.sqrt(variance)
    
    return avg, sd


def iterate_all(A, n, networks):
    
    allPoints = []
    
    for i in range(len(networks) - 2):
        for j in range(i + 1, len(networks) - 1):
            for k in range(j + 1, len(networks)):
                triplet = [networks[i], networks[j], networks[k]]
                data = do_trilaterate(A, n, triplet)
                
                if data[0] != -1:
                    allPoints.append(data)
                    
    sdCount = 2
    pointDifference = 999

    while pointDifference != 0:
        originalPointCount = len(allPoints)
        avg, sd = get_stats(allPoints)
        
        newPoints = [point for point in allPoints if distance(avg, point) < sdCount * sd]
        pointDifference = originalPointCount - len(newPoints)
        
        if pointDifference != len(allPoints):
            allPoints = newPoints
        else:
            pointDifference = 0
            
    pointSum = [sum(i) for i in zip(*allPoints)]
    
    return [pointSum[0] / len(allPoints), pointSum[1] / len(allPoints)]
                    


# In[16]:


# gets and processes error for the chosen scan location/floor/all data
def err_controller(A, n):
    err_bound = (0, 1e-4)
    err_total = 0.0
    levels = [2]
    
    # for each level we want to do this on...
    for level in levels:
        level_data = ap_dict[level]
        
        # for each sample location... (10 per floor 0:3, 6 on floor 4, 3 on floor 5)        
        for actual_point, scans in level_data.items():
            
            # for each of the 10 scans in that location...
            for scan in scans:
                
                # get the calculated location using trilat, and get dist to actual point
                predicted_point = iterate_all(A, n, scan)
                err = distance(predicted_point, actual_point)
                
                # error function?
                err_total += err
                
            # average error
            err_total = err_total / len(level_data.items())
                
    if err_total < err_bound[0]:
        err_total = err_bound[0]
    if err_total > err_bound[1]:
        err_total = err_bound[1]
            
    return err_total
    
    


# In[17]:


# function that obtains all the Z axis data, for a given A/n
def f_trilat(A_space, n_space):
    
    Z = []
    min_err = {'err': 9999, 'A': -1, 'n': -1}
    parameters = []
    
    for A_i, A in enumerate(A_space):
        Z_sub = []
        for n_i, n in enumerate(n_space):
            print(f"\rWorking on A {A_i+1}/{A_div} n {n_i+1}/{n_div}                                          ", end='')
            err = err_controller(A, n)
    
            if err < min_err['err']:
                min_err['err'] = err
                min_err['A'] = A
                min_err['n'] = n

            Z_sub.append(err)
        Z.append(Z_sub)

    print(f"\nMin err of {min_err['err']} at (A: {min_err['A']}; n: {min_err['n']})")
    
    return np.array(Z)


# In[20]:


A_div = 50
n_div = 50
A = np.linspace(-10, -50, A_div)
n = np.linspace(2, 4, n_div)
Z = f_trilat(A, n)

n, A = np.meshgrid(A, n)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel("A")
ax.set_ylabel("n")
ax.set_zlabel("Err")
ax.plot_surface(A, n, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')

plt.show()


# In[12]:
# In[ ]:





# In[ ]:




