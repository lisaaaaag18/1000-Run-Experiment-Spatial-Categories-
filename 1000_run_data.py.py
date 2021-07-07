import csv
import math
import pickle
import collections, functools, operator

def Conversions(file1, file2):
    '''
    file, file --> dict, dict

    This function reads a file in order to convert a zone to the appropriate planning 
    district. It then reads the second file to convert the planning districts to spatial
    categories. The function returns two dictionaries, the first one having the keys as
    zones and the values as the appropriate planning districts. The second dictionary has
    the planning districts as keys and spatial categories as values.

    '''
    zone_to_pd = {}
    pd_to_sp = {}    
    
    with open(file1, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for conversion_row1 in csv_reader:   
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1 
                zone_to_pd[conversion_row1[0]] = conversion_row1[1]
                
            
    with open(file2, 'r') as csv_file1:
        csv_reader1 = csv.reader(csv_file1, delimiter=',')
        line_count1 = 0
        for conversion_row2 in csv_reader1:
            if line_count1 == 0:
                line_count1 += 1
            else:
                line_count1 += 1
                pd_to_sp[conversion_row2[0]] = conversion_row2[1]
                   
    return (zone_to_pd, pd_to_sp)

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
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    sp_cars = {}
    riemann_sum = 0
    sd_list = []
    sc_deviations = {}
   
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                cars_list.append(int(row[5]))
                home_zone = row[1] 
                home_pd = variables[0][home_zone]
                home_sc = variables[1][home_pd]
                spatial_category_list.append(home_sc)
                

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
        
        for j in range (0, len(spatial_category_list), 1):
            if spatial_category_list[j] in sp_cars:
                sp_cars[spatial_category_list[j]].append(cars_list[j])
            else:
                sp_cars[spatial_category_list[j]] = [cars_list[j]] 

        for key in sp_cars:
            riemann_sum = 0
            for k in range (0, len(sp_cars[key]), 1):
                riemann_sum += (sp_cars[key][k] - sc_means[key])**2
            standard_deviation = math.sqrt(riemann_sum / len(sp_cars[key]))
            sd_list.append(standard_deviation)
            sc_deviations[key] = standard_deviation

        
        
    return sc_means 

#print(Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\households.csv'))

def Auto_Ownership_Mean_SD():
    dict_0 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv')
    dict_1 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv')
    dict_2 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\households.csv')
    dict_3 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\households.csv')
    dict_4 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\households.csv')
    dict_5 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\households.csv')
    dict_6 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\households.csv')
    dict_7 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\households.csv')
    dict_8 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\households.csv')
    dict_9 = Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\households.csv')

    filename="picklefile"
    with open(filename, 'wb') as fp:
        pickle.dump(dict_0,fp)
        pickle.dump(dict_1,fp)
        pickle.dump(dict_2,fp)
        pickle.dump(dict_3,fp)
        pickle.dump(dict_4,fp)
        pickle.dump(dict_5,fp)
        pickle.dump(dict_6,fp)
        pickle.dump(dict_7,fp)
        pickle.dump(dict_8,fp)
        pickle.dump(dict_9,fp)

    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    sd_dict = {}
    means_dict = {}
    totals_sum = {}
    sc_cd = {}

    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])

    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]

    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    for key in means_dict:
        value = sd_dict[key]/means_dict[key]
        sc_cd[key] = value

    return sc_cd

#print(Auto_Ownership_Mean_SD())


def Drivers_License(filename1, filename2):
    '''
    file --> dictionary

    This function calculates the fraction of people (16+ years old) who have a license in each spatial 
    category. It returns a dictionary where the keys are the spatial categories and the values are the 
    fraction of those people who have licenses in that spatial category.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    household_zones_dict = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    sp_license = {}
    total_people = {}

    with open (filename1, 'r') as csvfile1:
        file_reader1 = csv.reader(csvfile1, delimiter = ',')

        for row in file_reader1:
            household_zones_dict[row[0]] = row[1]
   
    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 

                
                if(row[0] in household_zones_dict):
                    if (int(row[2]) >= 16):
                        zone = household_zones_dict[row[0]]
                        planning_district = variables[0][zone]
                        spatial_category = variables[1][planning_district]
                        total_people[spatial_category] = total_people.get(spatial_category, 0) + 1
                        if(row[4] == 'true'):
                            sp_license[spatial_category] = sp_license.get(spatial_category, 0) + 1                        
                    

    sc_fraction = {k: sp_license.get(k, 0) / float(total_people[k]) for k in total_people}  
                  
    return sc_fraction
                    
#print(Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\persons.csv'))

def Mean_SD_Drivers_License():
    '''
    None --> dict

    This function saves the data collected from 10 runs of the Drivers_License function and stores each
    dictionary in a list. The data from that list is then used to calculate the mean and standard 
    deviation for each spatial category across 10 runs. It returns a dictionary where the keys are the 
    spatial categories and the values are the means / standard deviations for that spatial category.
    '''
    dict_0 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\persons.csv')
    dict_1 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\persons.csv')
    dict_2 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\persons.csv')
    dict_3 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\persons.csv')
    dict_4 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\persons.csv')
    dict_5 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\persons.csv')
    dict_6 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\persons.csv')
    dict_7 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\persons.csv')
    dict_8 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\persons.csv')
    dict_9 = Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\persons.csv')

    filename="picklefile"
    with open(filename, 'wb') as fp:
        pickle.dump(dict_0,fp)
        pickle.dump(dict_1,fp)
        pickle.dump(dict_2,fp)
        pickle.dump(dict_3,fp)
        pickle.dump(dict_4,fp)
        pickle.dump(dict_5,fp)
        pickle.dump(dict_6,fp)
        pickle.dump(dict_7,fp)
        pickle.dump(dict_8,fp)
        pickle.dump(dict_9,fp)


    #To load from pickle file
    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    sd_dict = {}
    means_dict = {}
    totals_sum = {}

    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    return (means_dict , sd_dict)

#print(Mean_SD_Drivers_License())

def Trip_Amounts(filename1, filename2):
    '''
    file --> dict

    This function calculates the amount of trips that occured every hour during the period of 12am
    to 12am the next day (24 hours) for each spatial category. The function returns a dictionary
    where the keys are the spatial categories and the values are a list where each element represents 
    the hour and how many trips occured in that hour, starting at 12 am.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    is_first_row1 = True
    bins = [0 for x in range (0,24)]
    start_list = []
    weight_list = []
    spatial_category_list = []
    household_zones_dict = {}
    sp_trip_quantity = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    sp_weights = {}
    output = {}
    
    with open (filename1, 'r') as csvfile1:
            file_reader1 = csv.reader(csvfile1, delimiter = ',')
    
            for row in file_reader1:
                if (is_first_row1 == True): #Checks if the row is the first row
                    is_first_row1 = False #Changes flag to false since there is only 1 first row    
                
                else: #If the row is not the first row             
                    household_zones_dict[row[0]] = row[1]    

    
    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                start_list.append(row[4])
                weight_list.append(row[6])
                
                if(row[0] in household_zones_dict):
                    zone = household_zones_dict[row[0]]
                    planning_district = variables[0][zone]
                    spatial_category = variables[1][planning_district]
                    spatial_category_list.append(spatial_category)                
                
    for j in range (0, len(spatial_category_list), 1):
        if spatial_category_list[j] in sp_trip_quantity:
            sp_trip_quantity[spatial_category_list[j]].append(start_list[j])
            sp_weights[spatial_category_list[j]].append(weight_list[j])
        else:
            sp_trip_quantity[spatial_category_list[j]] = [start_list[j]] 
            sp_weights[spatial_category_list[j]] = [weight_list[j]] 
            
    for key in sp_trip_quantity:
        bins = [0 for x in range (0,24)]
        for i in range (0, len(sp_trip_quantity[key]), 1):
            index = float(sp_trip_quantity[key][i])//60 % 24
            bins[int(index)] += float(sp_weights[key][i])  
            output[key] = bins
                
    return output

#print(Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trip_modes.csv'))
       
def Mean_SD_Trip_Amounts():
    dict_0 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trip_modes.csv')
    dict_1 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\trip_modes.csv')
    dict_2 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\trip_modes.csv')
    dict_3 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\trip_modes.csv')
    dict_4 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\trip_modes.csv')
    dict_5 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\trip_modes.csv')
    dict_6 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\trip_modes.csv')
    dict_7 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\trip_modes.csv')
    dict_8 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\trip_modes.csv')
    dict_9 = Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trip_modes.csv')

    filename="picklefile"
    with open(filename, 'wb') as fp:
        pickle.dump(dict_0,fp)
        pickle.dump(dict_1,fp)
        pickle.dump(dict_2,fp)
        pickle.dump(dict_3,fp)
        pickle.dump(dict_4,fp)
        pickle.dump(dict_5,fp)
        pickle.dump(dict_6,fp)
        pickle.dump(dict_7,fp)
        pickle.dump(dict_8,fp)
        pickle.dump(dict_9,fp)


    #To load from pickle file
    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_dict = {}
    means_dict = {}

    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals = [sum(x) for x in zip(*group_dict[key])]
        totals_dict[key] = totals

    for key in totals_dict:
        new_value = [x / len(group_dict[key]) for x in totals_dict[key]]
        means_dict[key] = new_value

    return means_dict

#print(Mean_SD_Trip_Amounts())

def Trip_Durations(filename1, filename2):
    '''
    file --> dict

    This function determines the average trip time for each spatial category by trip modes. It returns a nested
    dictionary where the keys are the spatial categories, and the values are dictionaries with keys being modes
    of transportation and values being the average trip time for that specific mode.

    '''
    is_first_row2 = True #Flag to check if the row in the file is the first row. Initialized as true
    is_first_row1 = True
    duration = 0
    durations_list = []
    household_zones_dict = {}
    weight_list = []
    spatial_category_list = []
    durations_dict = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    trip_type = []
    trip_type_dict = {}
    weights_dict = {}
    sp_weights = {}
    output_means = {}

    with open (filename1, 'r') as csvfile1:
        file_reader1 = csv.reader(csvfile1, delimiter = ',')

        for row in file_reader1:
            if (is_first_row1 == True): #Checks if the row is the first row
                is_first_row1 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row             
                household_zones_dict[row[0]] = row[1]
    
    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row2 == True): #Checks if the row is the first row
                is_first_row2 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                trip_type.append(row[3])
                duration = (float(row[5]) - float(row[4]))
                durations_list.append(duration)
                weight_list.append(float(row[6]))
                
                if(row[0] in household_zones_dict):
                    zone = household_zones_dict[row[0]]
                    planning_district = variables[0][zone]
                    spatial_category = variables[1][planning_district]
                    spatial_category_list.append(spatial_category)

    for i in range (0, len(spatial_category_list), 1):
            if (trip_type[i] not in trip_type_dict):
                trip_type_dict[trip_type[i]] = (durations_list[i] * weight_list[i])
                weights_dict[trip_type[i]] = weight_list[i]
                durations_dict[spatial_category_list[i]] = trip_type_dict
                sp_weights[spatial_category_list[i]] = weights_dict
                    
            else:
                trip_type_dict[trip_type[i]] += (durations_list[i] * weight_list[i])
                weights_dict[trip_type[i]] += weight_list[i]
                durations_dict[spatial_category_list[i]] = trip_type_dict
                sp_weights[spatial_category_list[i]] = weights_dict
                        
        
    for key in durations_dict:
        sc_means = {k: durations_dict[key][k] / float(sp_weights[key][k]) for k in durations_dict[key] if k in sp_weights[key]} 
        output_means[key] = sc_means
    
    return output_means

#print(Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trip_modes.csv'))

def Trip_Durations_Mean_Sd():  
    
    dict_0 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trip_modes.csv')
    dict_1 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\trip_modes.csv')
    dict_2 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\trip_modes.csv')
    dict_3 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\trip_modes.csv')
    dict_4 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\trip_modes.csv')
    dict_5 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\trip_modes.csv')
    dict_6 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\trip_modes.csv')
    dict_7 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\trip_modes.csv')
    dict_8 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\trip_modes.csv')
    dict_9 = Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trip_modes.csv')

    filename="picklefile"
    with open(filename, 'wb') as fp:
        pickle.dump(dict_0,fp)
        pickle.dump(dict_1,fp)
        pickle.dump(dict_2,fp)
        pickle.dump(dict_3,fp)
        pickle.dump(dict_4,fp)
        pickle.dump(dict_5,fp)
        pickle.dump(dict_6,fp)
        pickle.dump(dict_7,fp)
        pickle.dump(dict_8,fp)
        pickle.dump(dict_9,fp)

    #To load from pickle file

    data = []
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}

    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for i in range (0, len(data), 1):
        for key1 in data[i]:
            if (key1 in totals_dict):
                totals_dict[key1].append(data[i][key1])
                
            else:
                totals_dict[key1] = [data[i][key1]]
                
    for key in totals_dict:
        result = dict(functools.reduce(operator.add,
                 map(collections.Counter, totals_dict[key])))  
        
        sum_dict[key] = result
        
    for key in sum_dict:
        means_dict = {}
        for key1 in sum_dict[key]:
            means_dict[key1] = sum_dict[key][key1] / len(data)   
            final_means_dict[key] = means_dict
            
    return final_means_dict


#print(Trip_Durations_Mean_Sd())

def Shopping_Activities(filename):
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    d_act_list = []
    activities = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    shopping_amounts = {}
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                d_act_list.append(row[5])
                zone = row[6] 
                pd = variables[0][zone]
                if (pd != '0'):
                    sc = variables[1][pd]
                    spatial_category_list.append(sc)   
                    
                else:
                    spatial_category_list.append('0')
                  
                
    for i in range (0, len(spatial_category_list), 1):
        if (spatial_category_list[i] in activities):
            activities[spatial_category_list[i]].append(d_act_list[i])
                                
        else:
            activities[spatial_category_list[i]] = [d_act_list[i]]
            
    for key in activities:
        counter  = 0
        for j in range (0, len(activities[key]), 1):
            if (activities[key][j] == 'Market'):
                counter += 1
        shopping_amounts[key] = counter
    del(shopping_amounts['0'])         
    
    return shopping_amounts

#print(Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv'))

def Mean_SD_Shopping_Activities():
    dict_0 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trips.csv')
    dict_1 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\trips.csv')
    dict_2 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\trips.csv')
    dict_3 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\trips.csv')
    dict_4 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\trips.csv')
    dict_5 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\trips.csv')
    dict_6 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\trips.csv')
    dict_7 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\trips.csv')
    dict_8 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\trips.csv')
    dict_9 = Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv')

    filename="picklefile"
    with open(filename, 'wb') as fp:
        pickle.dump(dict_0,fp)
        pickle.dump(dict_1,fp)
        pickle.dump(dict_2,fp)
        pickle.dump(dict_3,fp)
        pickle.dump(dict_4,fp)
        pickle.dump(dict_5,fp)
        pickle.dump(dict_6,fp)
        pickle.dump(dict_7,fp)
        pickle.dump(dict_8,fp)
        pickle.dump(dict_9,fp)


    #To load from pickle file
    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_sum = {}
    means_dict = {}
    sd_dict = {}

    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    return sd_dict

#print(Mean_SD_Shopping_Activities())

def Other_Activities(filename):
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    d_act_list = []
    activities = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    other_amounts = {}
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                d_act_list.append(row[5])
                zone = row[6] 
                pd = variables[0][zone]
                if (pd != '0'):
                    sc = variables[1][pd]
                    spatial_category_list.append(sc)   
                    
                else:
                    spatial_category_list.append('0')
                  
                
    for i in range (0, len(spatial_category_list), 1):
        if (spatial_category_list[i] in activities):
            activities[spatial_category_list[i]].append(d_act_list[i])
                                
        else:
            activities[spatial_category_list[i]] = [d_act_list[i]]
            
    for key in activities:
        counter  = 0
        for j in range (0, len(activities[key]), 1):
            if (activities[key][j] == 'IndividualOther'):
                counter += 1
        other_amounts[key] = counter
    del(other_amounts['0'])         
    
    return other_amounts
#print(Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv'))

def Mean_Sd_Other_Activities():
    dict_0 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trips.csv')
    dict_1 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\trips.csv')
    dict_2 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\2\\Microsim Results\\trips.csv')
    dict_3 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\3\\Microsim Results\\trips.csv')
    dict_4 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\4\\Microsim Results\\trips.csv')
    dict_5 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\5\\Microsim Results\\trips.csv')
    dict_6 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\6\\Microsim Results\\trips.csv')
    dict_7 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\7\\Microsim Results\\trips.csv')
    dict_8 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\8\\Microsim Results\\trips.csv')
    dict_9 = Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv')

    filename="picklefile"
    with open(filename, 'wb') as fp:
        pickle.dump(dict_0,fp)
        pickle.dump(dict_1,fp)
        pickle.dump(dict_2,fp)
        pickle.dump(dict_3,fp)
        pickle.dump(dict_4,fp)
        pickle.dump(dict_5,fp)
        pickle.dump(dict_6,fp)
        pickle.dump(dict_7,fp)
        pickle.dump(dict_8,fp)
        pickle.dump(dict_9,fp)


    #To load from pickle file
    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_sum = {}
    means_dict = {}
    sd_dict = {}

    with open(filename, 'rb') as fr:
        try:
            while True:
                data.append(pickle.load(fr))
        except EOFError:
            pass

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    return sd_dict

#print(Mean_Sd_Other_Activities())

def School_Activities(filename1, filename2): #DOES NOT WORK YET
    household_zones_dict = {}
    is_first_row1 = True
    is_first_row2 = True
    student_stat_dict = {}
    d_act_list = [] 
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    spatial_category_list = []
    activities = {}
    school_amounts = {}
    households_list = []
    households_dict = {}
    total_amount = {}

    with open (filename1, 'r') as csvfile1:
        file_reader1 = csv.reader(csvfile1, delimiter = ',')

        for row in file_reader1:
            if (is_first_row1 == True): #Checks if the row is the first row
                is_first_row1 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row             
                student_stat_dict[row[0]] = row[9]

    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row2 == True): #Checks if the row is the first row
                is_first_row2 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                d_act_list.append(row[5])
                households_list.append(row[0])
                zone = row[6] 
                pd = variables[0][zone]
                if (pd != '0'):
                    sc = variables[1][pd]
                    spatial_category_list.append(sc)   
                    
                else:
                    spatial_category_list.append('0')

    for i in range (0, len(spatial_category_list), 1):
        if (spatial_category_list[i] in activities):
            activities[spatial_category_list[i]].append(d_act_list[i])
            households_dict[spatial_category_list[i]].append[households_list[i]]
                                
        else:
            activities[spatial_category_list[i]] = [d_act_list[i]]
            households_dict[spatial_category_list[i]] = [households_list[i]]
            
    for key in activities:
        counter  = 0
        for j in range (0, len(activities[key]), 1):
            if (activities[key][j] == 'School'):
                if (households_dict[key][j] in student_stat_dict):
                    student_stat = student_stat_dict[households_dict[key][j]]
                if (student_stat in school_amounts):
                    school_amounts[student_stat] += 1

                else:
                    school_amounts[student_stat] = 1
        total_amount[key] = school_amounts
        #shopping_amounts[key] = counter
    del(total_amount['0'])   

#print(School_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\persons.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trips.csv'))      