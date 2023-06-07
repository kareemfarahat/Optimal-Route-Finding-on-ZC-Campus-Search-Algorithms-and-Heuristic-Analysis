from Classes import *
from Algorithms import *
import tkinter as tk
import webbrowser


root=tk.Tk()
root.title("GUI")
# setting the windows size
root.geometry("600x270")

# make the window alwayes on top 
root.wm_attributes("-topmost", 1)


# declaring variable
Longitude_var=tk.DoubleVar()
Latitude_var=tk.DoubleVar()
init_place_var=tk.StringVar()
Longitude_des_var=tk.DoubleVar()
Latitude_des_var=tk.DoubleVar()
des_pLace_var=tk.StringVar()
seach_type_var=tk.StringVar()

search_alg = ["A*", "BFS", "DFS", "IDS","Greedy","hill climbing", "simulated annealing"]

# Button preview to display clean map for the user to enter data from
def preview():
   webbrowser.open_new_tab('index.html')

#Reset button
def reset():
   Longitude_var.set("")
   Latitude_var.set("")
   init_place_var.set("")
   Longitude_des_var.set("")
   Latitude_des_var.set("")
   des_pLace_var.set("")
   seach_type_var.set("") 

# Here we go:
def submit():
    # Handling whether locations are coordinates or places
    intial_location = init_place_var.get()
    destination_location = des_pLace_var.get()
    if intial_location  =="":
        start = [Longitude_var.get(),Latitude_var.get()]
        stop = [Longitude_des_var.get(),Latitude_des_var.get()]

        intial_location = redirect(start)
        destination_location = redirect(stop)
    # Hnadling if the user misentered data
    if seach_type_var.get() not in ["A*", "BFS", "DFS", "IDS","Greedy","hill climbing", "simulated annealing","DLS","API"]:
        top= tk.Toplevel(root)
        top.geometry("600x270")
        top.title("Warning")
        tk.Label(top, text= "please Enter a valid search algorithm", font=('Mistral 18 bold')).place(x=100,y=80)
        playsound("Omar.wav")
    else:
    # Switch over different algorithm
        #A star algorithm
        if seach_type_var.get() == "A*" : 
            path = A_star_search(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')
        # breadth first search algorithm
        elif seach_type_var.get() == "BFS" :
            path = bfs_graph(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')

        # Depth first search algorithm
        elif seach_type_var.get() == "DFS" :  
            path = dfs_graph(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')
        # Itirative depth search
        elif seach_type_var.get() == "IDS" :
            path = Ids_tree(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')
        # Greedy best first search algorithm
        elif seach_type_var.get() == "Greedy" :    
            path = greedy_best_first(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')
        # Hill climbing search algorithm
        elif seach_type_var.get() == "hill climbing" :
            path = hill_climbing(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')
        # Depth limited search
        elif seach_type_var.get() == "DLS" :         
            path = dls_tree(Map(intial_location,destination_location))
            top= tk.Toplevel(root)
            top.geometry("800x270")
            top.title("Path actions")
            tk.Label(top, text= str(path[0])+" with cost: "+str(path[1]) , font=('Mistral 10 bold')).place(x=5,y=80)            
            visualize_path(path,Road_dict).save("solution.html")
            webbrowser.open_new_tab('solution.html')
        # Using API request to identify the path:
        elif seach_type_var.get() == "API" :         

            path = find_path_with_api(str(Longitude_var.get())+","+str(Latitude_var.get()),\
                                      str(Longitude_des_var.get())+","+str(Latitude_des_var.get()))
            path.save("solution.html")
            webbrowser.open_new_tab('solution.html')
        if path: playsound("Bravo_3leeek.wav")
        path = None

# Exit button
def Exit():
    root.quit()
     
#Take initial location from the user as coordinates:
Longitude = tk.Label(root, text = 'Longitude', font=('calibre',10, 'bold')).place(x=5, y=800//4-120)
Longitude_entry = tk.Entry(root,textvariable = Longitude_var, font=('calibre',10,'normal'),).place(x=100, y=800//4-120)

Latitude = tk.Label(root, text = 'Latitude', font=('calibre',10, 'bold')).place(x=5, y=830//4-90)
Latitude_entry=tk.Entry(root, textvariable = Latitude_var, font = ('calibre',10,'normal')).place(x=100, y=830//4-90)


#Take destination location from the user as coordinates:
Longitude_des = tk.Label(root, text = 'Destination longitude', font=('calibre',10, 'bold')).place(x=250, y=800//4-120)
Longitude_des_entry = tk.Entry(root,textvariable = Longitude_des_var, font=('calibre',10,'normal')).place(x=400, y=800//4-120)

Latitude_des = tk.Label(root, text = 'Destination latitude', font=('calibre',10, 'bold')).place(x=250, y=830//4-90)
Latitude_des_entry=tk.Entry(root, textvariable = Latitude_des_var, font = ('calibre',10,'normal')).place(x=400, y=830//4-90)

#other way
init_pLace = tk.Label(root, text = 'Initial place', font=('calibre',10, 'bold')).place(x=5, y=860//4-60)
init_pLace_entry=tk.Entry(root, textvariable = init_place_var, font = ('calibre',10,'normal')).place(x=100, y=860//4-60)

des_pLace = tk.Label(root, text = 'Destination place', font=('calibre',10, 'bold')).place(x=250, y=860//4-60)
des_pLace_entry=tk.Entry(root, textvariable = des_pLace_var, font = ('calibre',10,'normal')).place(x=400, y=860//4-60)

#specify the type of search
search_alg = tk.Label(root, text = 'Type of search', font=('calibre',10, 'bold')).place(x=225, y=890//4-30)
search_alg_entry=tk.Entry(root, textvariable = seach_type_var, font = ('calibre',10,'normal')).place(x=325, y=890//4-30)

#buttons needed
sub_btn=tk.Button(root,text = 'Submit', command = submit).place(x=275, y=920//4)
preview_but=tk.Button(root,text = 'Preview', command = preview).place(x=200, y=920//4)
Reset_but=tk.Button(root,text = 'Reset', command = reset).place(x=350, y=920//4)
Exit_but=tk.Button(root,text = 'Exit', command = Exit).place(x=450, y=920//4)




# performing an infinite loop
# for the window to display
root.mainloop()
