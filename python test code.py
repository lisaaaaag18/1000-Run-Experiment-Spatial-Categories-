import csv
import math
import matplotlib.pyplot as plt
import numpy as np

def Conversions(file1, file2):
    zones_list = []
    zone_to_pd = {}
    pd_list = []
    zones_list_for_pd = []
    values_list = []
    sp_list = []
    pd_list2 = []
    pd_list_for_sp = []
    values_list2 = []
    pd_to_sp = {}    
    
    with open(file1, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for conversion_row1 in csv_reader:   
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1 
                zones_list.append(int(conversion_row1[0]))
                pd_list.append(int(conversion_row1[1]))
                
                
        for i in range (0, max(pd_list)+1, 1):
            
            zones_list_for_pd = []
            for j in range (0, len(pd_list), 1):
                if(pd_list[j] == i):
                    zones_list_for_pd.append(zones_list[j])
                    
            values_list.append(zones_list_for_pd)
            
        for k in range (0, max(pd_list)+1, 1):
            zone_to_pd[k] = values_list[k]
            
    with open(file2, 'r') as csv_file1:
        csv_reader1 = csv.reader(csv_file1, delimiter=',')
        line_count1 = 0
        for conversion_row2 in csv_reader1:
            if line_count1 == 0:
                line_count1 += 1
            else:
                line_count1 += 1
                sp_list.append(int(conversion_row2[1]))
                pd_list2.append(int(conversion_row2[0]))
                
        for i in range (0, max(sp_list)+1, 1):
                    
            pd_list_for_sp = []
            for j in range (0, len(sp_list), 1):
                if(sp_list[j] == i):
                    pd_list_for_sp.append(pd_list2[j]) 
                            
            values_list2.append(pd_list_for_sp)
                    
        for k in range (0, max(sp_list) + 1, 1):
            pd_to_sp[k] = values_list2[k]   
            
            
    return (values_list, values_list2, zone_to_pd, pd_to_sp)

def Auto_Ownership(filename): 
    '''
    file --> dictionary

    This function converts the zones where the houses are located into planning districts 
    and then spatial categries. Then, it calculates the average amount of cars contained in
    each household per spatial category. It returns a dictionary with the keys being the 
    spatial category and the values being the avaerage amount of cars per household in that 
    spatial category.

    '''   
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    cars_list = []
    cars = {}
    households = {}
    values_list = []
    values_list2 = []
           
              
                

                
                
      
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                cars_list.append(int(row[5]))
                for i in range (0, len(Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[0]), 1):
                    for j in range (0, len(Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[0][i]), 1):
                        if (int(row[1]) == Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[0][i][j]):
                            for key, value in Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[2].items():
                                if Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[0][i] == value:
                                    planning_district = key    
                                    
                            for k in range (0, len(Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[1]), 1):
                                for l in range (0, len(Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[1][k]), 1):
                                    if (planning_district == Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[1][k][l]):
                                        for key, value in Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[3].items():
                                            if Conversions('GTAModelV4ToPD.csv', 'PD_Spatial_Category_Conversion.csv')[1][k] == value:
                                                spatial_category = key 
                                                spatial_category_list.append(spatial_category)

        for i in range (0, len(cars_list), 1):
            if (spatial_category_list[i] not in cars):
                cars[spatial_category_list[i]] = cars_list[i]
                        
            else:
                cars[spatial_category_list[i]] += cars_list[i]
                
            if (spatial_category_list[i] not in households):
                households[spatial_category_list[i]] = 1
            
            else:
                households[spatial_category_list[i]] += 1
                
        sc_means = {k: cars[k] / float(households[k]) for k in cars if k in households}            
        
    return sc_means 

print(Auto_Ownership('test_1.csv'))
    