### importing libraries
import numpy as np
from statistics import median
import folium
import requests
import json
from playsound import playsound
with open('roads.json') as f:
    Road_dict = json.load(f)
# get every road coordinates list and git the median of the list

def get_road_rep(road=str, road_visual_dict=dict):
    x=[] # empty list to collect the x coordinates
    y=[] # empty list to collect the y coordinates
    for point in (road_visual_dict[road].get("features")[0].get("geometry").get("coordinates")):
      x.append(point[0])
      y.append(point[1])

    X= median(x) # get the median of x coordinates
    Y= median(y) # get the median of y coordinates
    return (X,Y) # return the x&y coordinat point as tuple
#  Heuristic_1 calculate the  Euclidean distance between 2 roads
   
def Heuristic_1(road1=str,road2=str,road_visual_dict=dict ):
  r1 = np.array(get_road_rep(road1, road_visual_dict))
  r2 = np.array(get_road_rep(road2, road_visual_dict))
  return np.linalg.norm(r1 - r2) * 95000
#  Heuristic_2 calculate the Manhattan distance  between 2 roads

def Heuristic_2(road1=str,road2=str,road_visual_dict=dict ):
  r1 = np.array(get_road_rep(road1, road_visual_dict))  # get the median coordinates point as the road representative
  r2 = np.array(get_road_rep(road2, road_visual_dict)) # get the median coordinates point as the road representative
  return (abs(r1[0] - r2[0]) + abs(r1[1] - r2[1])) * 95000 # return the Manhattan distance between 2 points and multiply it by the map ket ratio to return it in Meters


# function the visualizes the solution actions and costs on the map
# get the path and dict that contaoins roads coordinates lists
def visualize_path(path=tuple, road_visual=dict):
  center = [29.941725,31.067126] ## the map center so it starts on top of Zewail City
  m = folium.Map(location=center, zoom_start=16)  # request a map
  N_path= [] #empty array that will be filled with the roads that will be displayed on the map

  for node in path[0]: # loop over the actions list
    node = node.split(":")[1] # split in ":" and get the seconded elelment as it is equal to the state name
    if node in road_visual: # chek if the state has coordinates and is in the dictionary
      N_path.append(node) # append  the states that will be displayed on the map
  
  for j, p in enumerate(N_path):  # loop over the states that will be displayed on the map
      json = road_visual[p]  # get the json object if the state 
      dc = json.get("features")[0].get("geometry").get("coordinates") # get the Coordinates list
      if len(dc) == 1: #check if the coordinate list has single point so it is not a road and it will be  displayed as a marker
        dc[0][1], dc[0][0] = dc[0][0] , dc[0][1]
        folium.Marker(dc[0], tooltip="cross point", icon=folium.Icon(color="green", icon="flag")).add_to(m) # draw a marker on the map
      else:
        for i in range(len(dc)): # loop over the Coordinates list
          dc[i][1], dc[i][0] = dc[i][0] , dc[i][1]  # swap the points as folium is taking the values inverted

        if j == len(N_path) - 1: #check the end of the solution path to add a marker "Destination point"
          folium.Marker(dc[-1], tooltip="Destination point",icon=folium.Icon(color="red", icon="flag")).add_to(m)
        # draw the road on the lap as a line
        folium.PolyLine(dc,
                        color='blue',
                        weight=6,
                        opacity=0.8 , tooltip="Follow me ^^",smooth_factor=0.5).add_to(m)
        m.add_child(folium.LatLngPopup())
      
  return m  # return the map wath the path 







# function the  get to coordinates point from the user as a start and Destination 
# then request openrouteservice api to find the path and return a map with the path to the user
def find_path_with_api(start=str,end=str):  
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    link = "https://api.openrouteservice.org/v2/directions/" # the api ling
    typ = "foot-walking?" # tupe on navigation can be walking or car or whatever
    key = "api_key=5b3ce3597851110001cf6248a25bfff2d390457faf04afc0010647f3&" # the api key that need to be update every while 

    start = "start=" + start +"&"  # get the start point coordinates in the format start=x,y&
    end ="end=" + end # get the end point coordinates in the format end=x,y


    call = requests.get(link+ typ+ key+ start+end , headers=headers) # request the solution from openrouteservice api
    json = call.json() # get the request as json object
    dc = json.get("features")[0].get("geometry").get("coordinates") # get the Coordinates list of the object
    for i in range(len(dc)): # loop over the Coordinates list
        dc[i][1], dc[i][0] = dc[i][0] , dc[i][1] # swap the points as folium is taking the values inverted

        
    center = [29.941725,31.067126]   ## the map center so it starts on top of Zewail City
    m = folium.Map(location=center, zoom_start=16) # request a map from folium

    #In order to visualise every path the algorithm would try, add the following path while u have the coordinate of the path:
    #folium.Marker("visited location!", tooltip="start point", icon=folium.Icon(color="red", icon="question-sign")).add_to(m)

    folium.Marker(dc[0], tooltip="start point", icon=folium.Icon(color="blue", icon="plane")).add_to(m) # add a marker "Start point"
    folium.Marker(dc[-1], tooltip="Destination point",icon=folium.Icon(color="red", icon="flag")).add_to(m) # add a marker "Destination point"
     # draw the road on the lap as a line
    folium.PolyLine(dc,
                    color='blue',
                    weight=3,
                    opacity=0.8 , tooltip="Follow me ^^",smooth_factor=0.1).add_to(m)
    m.add_child(folium.LatLngPopup()) # add pop ap that disply the latitude and longitude of anay cliked point on the map as a popup
    return m # return the map whit the path displyed on it 




def redirect(my_location=list):
  """Map user location to the nearest predefined paths """
  nearest_node = ""
  #lowest initialized by any number greater than 1

  lowest = 1000
  f = open('roads.json')
  #Iterate over each node and return the nearst node and remap the user location to it
  road_visual_dict = json.load(f)
  for node in road_visual_dict.keys():
      node_path = road_visual_dict[node].get("features")[0].get("geometry").get("coordinates")
      for point, _ in  enumerate(node_path):
        diff = abs(node_path[point][0]-my_location[0])+ abs(node_path[point][1]-my_location[1])
        if diff < lowest:
          lowest = diff
          nearest_node = node
  f.close()
  return (nearest_node)
