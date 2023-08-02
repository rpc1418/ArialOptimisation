from ctypes import pointer
import os
import sys
import subprocess

try :
    import math
except:
    completed = subprocess.run(["powershell", "-Command", 'pip install math'], capture_output=True)
    import math


try :
    import csv
except:
    completed = subprocess.run(["powershell", "-Command", 'pip install csv'], capture_output=True)
    import csv


try :
    import pandas as pd
except:
    completed = subprocess.run(["powershell", "-Command", 'pip install pandas'], capture_output=True)
    import pandas as pd


try :
    import collections
except:
    completed = subprocess.run(["powershell", "-Command", 'pip install collections'], capture_output=True)
    import collections


try :
    import heapq
except:
    completed = subprocess.run(["powershell", "-Command", 'pip install heapq'], capture_output=True)
    import heapq

try :
    import plotly.express as px
except:
    completed = subprocess.run(["powershell", "-Command", 'pip install plotly'], capture_output=True)
    import plotly.express as px


def csvtolistofdict_file_extractor(location):
    myFile = open(os.path.join(sys.path[0], location), 'r')
    reader = csv.DictReader(myFile)
    airplanes  = list() # airplanes and their coordinates and altitude
    float_column_index = 2
    for dictionary in reader:
        airplanes.append(dictionary)
    return airplanes
dataset_loacation="dataset.CSV"
airplanes=csvtolistofdict_file_extractor(dataset_loacation)

def shortestPath(edges, source, sink):
    # create a weighted DAG - {node:[(cost,neighbour), ...]}
    graph = collections.defaultdict(list)
    for l, r, c in edges:
        graph[l].append((c,r))
    # create a priority queue and hash set to store visited nodes
    queue, visited = [(0, source, [])], set()
    heapq.heapify(queue)
    # traverse graph with BFS
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        # visit the node if it was not visited before
        if node not in visited:
            visited.add(node)
            path = path + [node]
            # hit the sink
            if node == sink:
                return (cost, path)
            # visit neighbours
            for c, neighbour in graph[node]:
                if neighbour not in visited:
                    heapq.heappush(queue, (cost+c, neighbour, path))
    return float("inf")


def calculate_distance(coord1, coord2):
    # Calculate distance using Haversine formula
    lat1 = math.radians(float(coord1['latitude']))
    lon1 = math.radians(float(coord1['longitude']))
    lat2 = math.radians(float(coord2['latitude']))
    lon2 = math.radians(float(coord2['longitude']))

    dlon = lon2 - lon1
    dlat = lat2 - lat1  

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    radius = 6371  # Radius of the Earth in kilometers
    distance = radius * c
    return distance
# Calculate altitude difference
    altitude_diff = abs(alt2 - alt1)

    # Add altitude difference to the distance
    total_distance = math.sqrt(distance*2 + altitude_diff*2)

    return total_distance



def calculate_data_rate(distance):
    if(distance>500):
        return 31.895
    
    elif(400<distance<500):
        return 43.505
    
    elif(300<distance<400):
        return 52.857
    
    elif(190<distance<300):
        return 63.970
    
    elif(90<distance<190):
        return 77.071
    
    elif(35<distance<90):
        return 93.854
    
    elif(5.56<distance<35):
        return 119.130
    
    else:
        return 200.0
     # Returns a constant data rate for simplicity for distance less then 5.56km
    


def find_all_routing_path():
    routing_path = []    
    
    for airplane1 in airplanes:
        aplist=[]
        for airplane2 in airplanes:
            
            distance = calculate_distance(airplane1,airplane2)
            data_rate = calculate_data_rate(distance)
            if(airplane1!=airplane2):
                edge=(airplane1['name'],airplane2['name'],int(distance))
                routing_path.append(edge)
    return routing_path               
allroutingpath=find_all_routing_path()  

def shortest_routing_path():
    ptogs=[]
    

    for ap in airplanes:
        a=shortestPath(allroutingpath,ap['name'],'Newark Liberty')
        b=shortestPath(allroutingpath,ap['name'], "Heathrow")    
        if(a[0]>b[0]):
            ptogs.append(b)
        else:
            ptogs.append(a)
    return ptogs 
ptogs=shortest_routing_path()


#md is the longest distance in the optimal path and hence Datarate of(md) is maximum possible transmission rate
#lc is the latency here


def transmission_rate():
    trrate=[]
    trrate.append(('Source','[Base Node,Next Route Data-rate]','Nearest Ground Station and Lastnode','End-To-End Data-rate','Latency'))

    for a in ptogs:
        for b in a[1]:
            md=0
            lc=0
            routeadd=[]
            for c in a[1]:   
                lc+=50
                for edge in allroutingpath:
                    if((edge[0]==b)&(edge[1]==c)):
                        d=edge[2]
                        addnode=[edge[1],calculate_data_rate(d)]
                        routeadd.append(addnode)
                        if(md<d):
                            md=d
                            
        z=a[1]
        
        trrate.append((z[0],routeadd,z[-1],calculate_data_rate(md),lc-50))
    return trrate
trrate=transmission_rate()

#writingfiles
mydf=pd.DataFrame(allroutingpath)
mydf.to_csv('all_Paths_Available.csv', index=False, header=False)

mydf2=pd.DataFrame(trrate)
mydf2.to_csv('Final_result.csv', index=False, header=False)

mydf2=pd.DataFrame(ptogs)
mydf2.to_csv('ptogs.csv', index=False, header=False)


def tocheck():
    a=input('Enter the flight name:')
    for i in trrate:
        if (a==i[0]):
            print(i[0],',routing path:',i[1],',End-to-End DataRate:',i[3],',Latency:',i[4])
    input('Press enter to see paths of all the flights.')

tocheck()

def plot():
    flightname=[]
    nodelist=[]
    latitudelist=[]
    longitudelist=[]
    for flight in ptogs:
        path=flight[1]
        for node in path:
            nodelist.append(node)
            for i in airplanes:
                if(i['name']==node):
                    latitudelist.append(float(i['latitude']))
            for i in airplanes:
                if(i['name']==node):
                    longitudelist.append(float(i['longitude']))
            flightname.append(path[0])

    dictdata={'flightname':flightname,'nodename':nodelist,'latitude':latitudelist,'longitude':longitudelist}
    dataf=pd.DataFrame(dictdata)


    #for node plot
    df = pd.read_csv(open(os.path.join(sys.path[0], "dataset.CSV"), 'r'))
    fig = px.scatter_mapbox(df,lat='latitude',lon='longitude', hover_name="name")
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41,
        margin={"r":0,"t":0,"l":0,"b":0})

    #for path plot
    fig2= px.line_mapbox(dataf, lat="latitude", lon="longitude",color="flightname",hover_name="nodename",)
    fig2.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41,
        margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    fig2.show()

plot()

