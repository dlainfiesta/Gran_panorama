# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%% Paths

import os

print(os.getcwd())
path= 'C:\\Users\\diego\\Desktop\\DL\\Covid_Guatemala\\Gran_panorama\\Modelo'
os.chdir(path)
print(os.getcwd())

path_input= path+'\\01_Input\\'
path_code= path+'\\02_Code\\'
path_output= path+'\\03_Output\\'

#%% Importing packages

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import pandas as pd
from datetime import datetime
import numpy as np
import random
import pickle

#%% Parameters

# Transimission rate ro= 2.2, in a group of 5 infected, 4 infected, infect additional 8, and 1 infects 3. 
# resulting probabilities of quantitiy

to_contage_before= np.array([2, 2, 2, 2, 3])
to_contage_after= np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0])

# Scenarios
scenarios= 1000

# Total population
total_population= 17915567

# Stopping condition
infected_percentage= 0.90

# Infected ensemble solution
infected_ensemble_solution= []

# Infected Fatality Rate (IFR)
IFR= 0.75/100

# Vaccine parameters
time_for_vaccine= 16 #months Here we select 12 or 16 months.
lead_time_for_vaccine= 3 #months

# Week of the year for introducting shock measures:
instant_shock_measures= 11 # Week of the year

#%% Simulating weeks, each time slot is 1 week
    
# Initial infected
   
infected_ensemble= []
initial_condition= [1]

for k in range(scenarios):
    
    print('Now doing scenario:', k)
    
    infected_run= initial_condition.copy()
    
    i= 0
    
    while len(infected_run) <= (time_for_vaccine+lead_time_for_vaccine)*(52/12):
            
        new_contagions= 0
            
        if len(infected_run) <= instant_shock_measures:
        
            for j in range(infected_run[i]):
                
                new_contagions+= to_contage_before[random.randint(0, len(to_contage_before)-1)]
                
            infected_run.append(new_contagions)
                
            i+= 1

        else:
            
            for j in range(infected_run[i]):
                
                new_contagions+= to_contage_after[random.randint(0, len(to_contage_after)-1)]
                
            infected_run.append(new_contagions)
