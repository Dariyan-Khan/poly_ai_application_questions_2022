#A node consists of an x coordinate, y coordinate, and z coordinate 
from math import sqrt,inf
import heapq
import copy

class Node:
    def __init__(self,name,x,y,z):
        self.name=name
        self.x=x
        self.y=y
        self.z=z

#Create node objects for each station
def create_nodes(zearth_x,zearth_y,zearth_z,N, coord_list):
    
    #We treat our start (Zearth) as node 0 and our end (Earth) as node 1.
    node_dict={0:Node(1,zearth_x,zearth_y,zearth_z), 1:Node(0,0,0,0)}
    #Add in rest of stations
    for num in range(0,N):
        node_dict[num+2]=Node(num+2,coord_list[3*num],coord_list[3*num+1],coord_list[3*num+2])
        
    return node_dict


#calculates euclidean distance between two stations
def node_dist(A,B):
    return sqrt((A.x-B.x)**2 + (A.y-B.y)**2 + (A.z-B.z)**2)


#Create dictionary of distances between nodes
def dist_dict(total_nodes,nodes_dict):
    full_dist_dict={}
    for current_node in range(total_nodes):
        current_dist_dict={}
        
        #As our graph is undirected, the distance from A to B = distance from B to A
        #This allows us to save calls to our node_dist function, which is what the for loop below reflects.
        for prev_node in range(0,current_node):
            current_dist_dict[prev_node]=full_dist_dict[prev_node][current_node]
        
        for next_node in range(current_node+1,total_nodes):
            current_dist_dict[next_node]=node_dist(nodes_dict[current_node],nodes_dict[next_node])
        
        full_dist_dict[current_node]=current_dist_dict
    
    return full_dist_dict



#We use a modified version of djikstras algorithm, where instead of keeping track of thee shortest distance
#between two points, we track the maximum required teleportation needed to get between them.
def djikstra(total_nodes,nodes_dict,full_dist_dict):
    max_dist={0:0}
    priority_q=[]
    #set maximum teleportation length to infinity initially
    for node in range(1,total_nodes):
        max_dist[node]=inf
    visited=[0]
    current_node=0
    
    while 1 not in visited: #only care about the max distance from 0 to 1
        
        for node in range(total_nodes): 
            if (node!=current_node) and (node not in visited):
                distance=full_dist_dict[current_node][node]
                #see if this new path or the stored path has a shorter max teleportation
                if max(max_dist[current_node],distance)<max_dist[node]:
                    max_dist[node]=distance
                    #we use a priority queue for efficiency and ease
                    heapq.heappush(priority_q,(distance,node))
        
        next_node=0
        while next_node in visited:
            #We find the next unvisited node with the shortest max teleportation from 0
            next_node=heapq.heappop(priority_q)[1]
        
        current_node=copy.copy(next_node)
        visited.append(current_node)
    
    return max_dist 
    
def shortest_teleport(zearth_x,zearth_y,zearth_z,N,*args):
    total_nodes=N+2
    
    nodes_dict=create_nodes(zearth_x,zearth_y,zearth_z,N,args)
    
    full_dist_dict=dist_dict(total_nodes,nodes_dict)
    
    max_teleport_dist=djikstra(total_nodes,nodes_dict,full_dist_dict)
    
    return round(max_teleport_dist[1],2)

#test
#print(shortest_teleport(-4,0,0,2,-3,0,0,-2,-2,-2))
