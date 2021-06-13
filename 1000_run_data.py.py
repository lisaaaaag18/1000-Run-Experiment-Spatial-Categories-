import csv
import math

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
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                cars_list.append(int(row[5]))
                
                with open('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for conversion_row1 in csv_reader:   
                        if line_count == 0:
                            line_count += 1
                        else:
                            line_count += 1
                            if(row[1] == conversion_row1[0]):
                                planning_district = conversion_row1[1]
                                
                                with open('C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv', 'r') as csv_file1:
                                    csv_reader1 = csv.reader(csv_file1, delimiter=',')
                                    line_count1 = 0
                                    for conversion_row2 in csv_reader1:
                                        if line_count1 == 0:
                                            line_count1 += 1
                                        else:
                                            line_count1 += 1
                                            if (planning_district == conversion_row2[0]):
                                                spatial_category = conversion_row2[1]
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
                
        print(cars)
        print(households)
        sc_means = {k: cars[k] / float(households[k]) for k in cars if k in households}            
        
    return sc_means 

print(Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv'))


def Drivers_License(filename):
    '''
    file --> dictionary

    This function calculates the fraction of people of each age who have a license.
    It returns a dictionary where the keys are the ages and the values are the fraction
    of those people who have licenses.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    ages_list = []
    ages_dict = {}
    licenses_list = []
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                ages_list.append(row[2]) 
                if(row[4] == 'true'):
                    licenses_list.append(1)
                else:
                    licenses_list.append(0)

        for i in range (0, len(ages_list),1):
            if(ages_list[i] not in ages_dict):
                ages_dict[ages_list[i]] = float(licenses_list[i])

            else:
                value = ages_dict[ages_list[i]]
                value += licenses_list[i]
                ages_dict[ages_list[i]] = value

        for key in ages_dict:
            value = ages_dict[key]/len(ages_list)    
            ages_dict[key] = value    
    return ages_dict
                    
#print(Drivers_License('C:\\Users\\gusevael\\Downloads\\test_1.csv'))

def Number_of_Trips(filename):
    '''
    file --> list

    This function calculates the amount of trips that occured every hour during the period of 12am
    to 12am the next day (24 hours). The amount of trips each hour is stored in a list where each element
    represents the hour, starting at 12 am. The data is then saved to a file which will be used for further 
    calculations.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    bins = [0 for x in range (0,24)]

    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                index = float(row[4])//60 % 24
                bins[int(index)] += float(row[6])
                
    

    F=open('C:\\Users\\gusevael\\Downloads\\trip_list_data.csv','a')

    for k in range (0, len(bins), 1):
        F.write(str(bins[k]) + " ")
    F.write("\n")

    F.close()

    return bins

#print(Number_of_Trips('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trip_modes.csv'))

def Trip_Durations(filename):
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    duration = 0
    counter = 0
    durations_list = []
    riemann_sum = 0
    total_duration = 0
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                duration = (float(row[5]) - float(row[4]))
                total_duration += duration
                counter += 1
                durations_list.append(duration)

        mean_duration = total_duration/counter

    for i in range (0, len(durations_list), 1):
        riemann_sum += (durations_list[i] - mean_duration)**2 #Calculates the riemann sum part of the standard deviation
        
    standard_deviation = math.sqrt(riemann_sum / counter) #Calculates standard deviation
    return  (mean_duration, standard_deviation)


#print(Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trip_modes.csv'))