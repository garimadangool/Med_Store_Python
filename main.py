    '''
    This is the main program

    This program displays , sells , restocks , saves all sata to files
    also gives the option to exit the program

    Reads initial data from the file and updates to
    medicines_updated.txt

    It imports varipus functions:
    read_data, write_data,sell_medicine, restock_medicine, display
    '''

#importing functions from other files
from read_data import read_data 
from write_data import write_data
from operations import  sell_medicine, restock_medicine
from display import display

data = read_data("medicines.txt") #load data from file into dictionary

if data is None:
    print("System cannot continue without data file.")
    exit()


while True: #infinite loop
    #Display menu option
    print("\n1. Display Medicines")
    print("2. Sell Medicine")
    print("3. Restock Medicine")   
    print("4. Exit")

    choice = input("Enter choice: ") #Takes Input from User

    #Option 1: Display medicines
    if choice == "1":
        display(data) #calls display function

    # Option 2: Sell medicine
    elif choice == "2":
        sell_medicine(data) # update stock after selling
        
        write_data("medicines_updated.txt", data)  # save changes

    # Option 3: Restock medicine
    elif choice == "3":
        restock_medicine(data)
        write_data("medicines_updated.txt", data)  # save changes

    # Option 4: Exit program
    elif choice == "4":
        write_data("medicines_updated.txt", data) # final save before exit
        print("Thank you!")
        break # stops loop

    
    # Invalid input handling
    else:
        print("Invalid choice!")
