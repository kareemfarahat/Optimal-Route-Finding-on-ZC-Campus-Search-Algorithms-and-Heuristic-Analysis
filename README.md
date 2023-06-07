# Optimal-Route-Finding-on-ZC-Campus-Search-Algorithms-and-Heuristic-Analysis
Optimal Route Finding on ZC Campus: Search Algorithms and Heuristics. Explore the best route between locations on ZC campus using search algorithms (BFS, DFS, IDS), heuristics (Greedy, A*), and optimization techniques. Compare results and visualize solutions on ZC map.
Getting Started
1-Clone the repository:
git clone 
2-Install the required dependencies:
pip install -r requirements.txt
3- Add your API link and API key of the openrouteservice on the Functions.py
4- Run the GUI.py
python GUI.py
GUI.py: Contains the graphical user interface (GUI) code for the navigation system. It allows users to enter their location details and select a search algorithm for path finding.
Classes.py: Defines the classes used in the navigation system, including the Map class for representing the map and the Road class for representing road segments.
Algorithms.py: Contains various search algorithms implemented for finding the optimal path, such as A*, BFS, DFS, IDS, Greedy, Hill Climbing, DLS, and API-based search.
functions.py: Contains various utility functions used in the application.
actions.json: Provides a list of actions that can be performed in the navigation system, along with their associated costs.
roads.json: Describes the road network by providing information about road segments, including their start and end locations, length, and speed limits.
