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

path_input= path+'\\1.Input\\'
path_code= path+'\\2.Code\\'
path_output= path+'\\3.Output\\'

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

to_contage= np.array([2, 2, 2, 2, 3])

# Scenarios
scenarios= 100

# Total population
total_population= 17915567

# Stopping condition
infected_percentage= 0.90

# Infected ensemble solution
infected_ensemble_solution= []

#%% Simulating weeks, each time slot is 2 weeks.
    
# Initial infected
   
infected_ensemble= []
initial_condition= [1]

for k in range(scenarios):
    
    print('Now doing scenario:', k)
    
    infected_run= initial_condition.copy()
    
    i= 0
    while sum(infected_run)< total_population*infected_percentage:
            
        new_contagions= 0
            
        for j in range(infected_run[i]):

            new_contagions+= to_contage[random.randint(0, len(to_contage)-1)]
            
        infected_run.append(new_contagions)
            
        i+= 1
            
    infected_ensemble.append(infected_run)

# Determining duration of the spread
    
pandemic_duration= [len(scenario) for scenario in infected_ensemble]

pandemic_duration_average= sum(pandemic_duration)/len(pandemic_duration)

print('Contagion at the middle of the disease (1 week), the pandemic would last in Guatemala: %i months.' % (pandemic_duration_average/4))
print('Contagion at the end of the average disease duration (2 week), the pandemic would last in Guatemala: %i months.' % (pandemic_duration_average*2/4))

#%% Importing real data

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url,index_col=0,parse_dates=[0])

guatemala_raw= df[df['location']=='Guatemala']
guatemala_raw['week']= guatemala_raw['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').isocalendar()[1]).astype(int)

weekly_new_cases = pd.pivot_table(guatemala_raw, values='new_cases', index=['week'],\
                    aggfunc=np.sum)

# Letting lists with the same length withing pandemic duration

pandemic_duration_clean= []

for scenario in infected_ensemble:
     
    if len(scenario) < max(pandemic_duration):
        
        for i in range(max(pandemic_duration)-len(scenario)):
            scenario.append(np.nan)
           
        pandemic_duration_clean.append(scenario)
        
    else:
        pandemic_duration_clean.append(scenario)

# Making time lists for 1 week transmission and 2 week transmission

time= [min(weekly_new_cases.index)]

i= 0
time_2_weeks= time.copy()
while i < max(pandemic_duration)-1:
    time_2_weeks.append(time_2_weeks[i]+2)
    i+= 1
    
time_1_weeks= [min(weekly_new_cases.index)]

i= 0
time_1_weeks= time.copy()
while i <= max(pandemic_duration)-2:
    time_1_weeks.append(time_1_weeks[i]+1)
    i+= 1

results_2_w_df= pd.DataFrame({'week':time_2_weeks})

for i in range(len(pandemic_duration_clean)):
    string= 'Scenario'+str(i)
    results_2_w_df['new_cases_predicted_2_weeks_'+string]= pandemic_duration_clean[i]

results_2_w_df= results_2_w_df.set_index('week', drop= True)

results_1_w_df= pd.DataFrame({'week':time_1_weeks})

for i in range(len(infected_ensemble)):
    string= 'Scenario'+str(i)
    results_1_w_df['new_cases_predicted_1_weeks_'+string]= infected_ensemble[i]

results_1_w_df= results_1_w_df.set_index('week', drop= True)

#%% Plotting each scenario

results_2_w_truncated= results_2_w_df[results_2_w_df.index <= max(weekly_new_cases.index)+2]
results_1_w_truncated= results_1_w_df[results_1_w_df.index <= max(weekly_new_cases.index)+1]

# Con 1 semana

fig= plt.figure()

plt.plot(results_1_w_truncated.index, results_1_w_truncated, '-', color='mistyrose', linewidth= 1)
plt.plot(results_1_w_truncated.index, results_1_w_truncated.mean(axis= 1), '-', color= 'salmon', linewidth= 0.75)
plt.plot(weekly_new_cases.index, weekly_new_cases['new_cases'], 'o', color= 'royalblue', markersize= 4)

plt.xlabel('Semana del año 2020', fontsize= 10)
plt.ylabel('Casos nuevos (personas infectadas)', fontsize= 10)

plt.grid(True, which="both", linestyle='--')
plt.xticks(results_1_w_truncated.index, fontsize= 9)
plt.yticks(np.arange(0, max(np.max(results_1_w_truncated.values),max(weekly_new_cases['new_cases'])), 1000), fontsize= 9)

misty_patch = mpatches.Patch(color='mistyrose', label='Realizaciones - '+str(scenarios)+' escenarios')
salmon_patch = mpatches.Patch(color= 'salmon', label='Realizaciones promedio')
blue_patch = mpatches.Patch(color= 'royalblue', label='Reportados-¿real?')
plt.legend(handles=[misty_patch, salmon_patch, blue_patch], loc= 0, frameon= False)
plt.title('Casos nuevos 1 semana atraso contagio y Ro= 2.2')

plt.savefig(path_output+'naive_model_1_weeks_Ro_2.2.jpg', dpi= 1200)
plt.show()

# With 2 weeks

fig= plt.figure()

plt.plot(results_2_w_truncated.index, results_2_w_truncated, '-', color='azure', linewidth= 1)
plt.plot(results_2_w_truncated.index, results_2_w_truncated.mean(axis= 1), '-', color= 'teal', linewidth= 0.75)
plt.plot(weekly_new_cases.index, weekly_new_cases['new_cases'], 'o', color= 'royalblue', markersize= 4)

plt.xlabel('Semana del año 2020', fontsize= 12)
plt.ylabel('Casos nuevos (personas infectadas)', fontsize= 12)

plt.grid(True, which="both", linestyle='--')
plt.xticks(np.arange(min(results_2_w_truncated.index), max(results_2_w_truncated.index)+1, 1))
plt.yticks(np.arange(0, max(np.max(results_2_w_truncated.values),max(weekly_new_cases['new_cases'])), 100))

azure_patch = mpatches.Patch(color='azure', label='Realizaciones - '+str(scenarios)+' escenarios')
teal_patch = mpatches.Patch(color= 'teal', label='Realizaciones promedio')
blue_patch = mpatches.Patch(color= 'royalblue', label='Reportados-¿real?')
plt.legend(handles=[azure_patch, teal_patch, blue_patch], loc= 2, frameon= False)
plt.title('Casos nuevos 2 semanas atraso contagio y Ro= 2.2')

plt.savefig(path_output+'naive_model_2_weeks_Ro_2.2.jpg', dpi= 1200)
plt.show()

# Both 1 and 2 weeks

fig= plt.figure()

plt.plot(results_1_w_truncated.index, results_1_w_truncated, '-', color='mistyrose', linewidth= 1)
plt.plot(results_1_w_truncated.index, results_1_w_truncated.mean(axis= 1), '-', color= 'salmon', linewidth= 0.75)

plt.plot(results_2_w_truncated.index, results_2_w_truncated, '-', color='azure', linewidth= 1)
plt.plot(results_2_w_truncated.index, results_2_w_truncated.mean(axis= 1), '-', color= 'teal', linewidth= 0.75)

plt.plot(weekly_new_cases.index, weekly_new_cases['new_cases'], 'o', color= 'royalblue', markersize= 4)

plt.xlabel('Semana del año 2020', fontsize= 10)
plt.ylabel('Casos nuevos (personas infectadas)', fontsize= 10)

plt.grid(True, which="both", linestyle='--')
plt.xticks(np.arange(min(results_1_w_truncated.index), max(results_2_w_truncated.index)+1, 1))
plt.yticks(np.arange(0, max(np.max(results_1_w_truncated.values),max(weekly_new_cases['new_cases'])), 1000))

misty_patch = mpatches.Patch(color='mistyrose', label='Realizaciones 1 semana - '+str(scenarios)+' escenarios')
salmon_patch = mpatches.Patch(color= 'salmon', label='Realizaciones 1 semana promedio')

azure_patch = mpatches.Patch(color='azure', label='Realizaciones  2 semanas - '+str(scenarios)+' escenarios')
teal_patch = mpatches.Patch(color= 'teal', label='Realizaciones 2 semanas promedio')

blue_patch = mpatches.Patch(color= 'royalblue', label='Reportados-¿real?')

plt.legend(loc= 2, handles=[misty_patch, salmon_patch, azure_patch, teal_patch, blue_patch], frameon= False)
plt.title('Casos nuevos 1 y 2 semana/s atraso contagio y Ro= 2.2')

plt.savefig(path_output+'naive_model_1_2_weeks_Ro_2.2.jpg', dpi= 1200)
plt.show()

# Saving files

pickle.dump(infected_ensemble, open(path_output+"Ro_2.2_free_ensemble.p", "wb" ))
