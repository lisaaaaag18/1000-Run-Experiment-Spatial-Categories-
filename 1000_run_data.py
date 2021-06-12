import csv
import math

def Auto_Ownership(filename):    
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    total_cars = 0 #How many cars there are in total. Initialized as 0
    total_households = 0 #How many households there are in total. Initialized as 0
    max_cars = 4
    H_cars = [i*2 for i in range (0, max_cars + 1)]
    riemann_sum = 0 #Riemann sum used to calculate standard deviation
    vehicle_list = [] #Empty list use to store amunt of vehicles per household
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                cars_in_household = int(row[5]) 
                total_cars += cars_in_household
                H_cars[cars_in_household] += 1
                total_households += 1 #increases total household amount by 1
                vehicle_list.append(int(row[5])) #Adds amount of vehicles to vehicle list
                
                
        avg_auto_ownership = int(total_cars)/int(total_households) #Calculates the mean amount of cars per household
            
    for i in range (0, len(vehicle_list), 1): #Goes through the list of cars per household
        riemann_sum += (vehicle_list[i] - avg_auto_ownership)**2 #Calculates the riemann sum part of the standard deviation
        
    standard_deviation = math.sqrt(riemann_sum / total_households) #Calculates standard deviation
    return  standard_deviation

print(Auto_Ownership('households.csv'))

def Drivers_License(filename):
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    num_with_license = 0
    num_no_license = 0
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row   
                if (row[4] == 'true'):
                    num_with_license += 1
                    
                else:
                    num_no_license += 1
                    
    return num_with_license
                    
print(Drivers_License('persons.csv'))

def Number_of_Trips(filename):
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true

    trips_list = []
    row_counter = 0
    start_times_list = []

    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            row_counter = 0
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                start_times_list.append(row[4])
                
        for i in range (240, 1680, 24):
            trip_nums = 0
            for j in range (0, len(start_times_list), 1):
                if (float(start_times_list[j]) >= i and float(start_times_list[j]) < i + 24):
                    trip_nums += 1
                    
            trips_list.append(trip_nums)
                    

                
    return trips_list
print(Number_of_Trips('trip_modes.csv'))
    