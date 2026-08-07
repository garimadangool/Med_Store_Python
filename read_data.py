def read_data(file):

    '''
    This function reads information on medicine from the file and dtroes them in a dictionary.

    There must be 6 comma separated values in each valid line:
    name, company, stock,unit_price, strip_price, per_strip

    Returns:
    Dictionary with counter as key and medicine details as list
    '''
 
    data = {}  #Empty dictionary

    try:  #Starting of error handeling block
        
        f = open(file, "r")   # Opening file in read mode
        lines = f.readlines()
 
        counter = 1 #Assigning ID to each medicine
        
        for line in lines:
            parts = line.strip().split(",") #Creating a list

            if len(parts) != 6:
                print("Skipping invalid line:", line.strip())
                continue

            try:
                data[counter] = [  # Storing medicine data in dictionary
                    parts[0], #name
                    parts[1],  #brand
                    int(parts[2]), #stock(tablets)
                    int(parts[3]), #price per tablet
                    int(parts[4]), #price per strip
                    int(parts[5])  #tablets per strip
                ]
                counter += 1 #Moving to next ID for next medicine

            except ValueError:   #Runs if exception occurs
                print("Invalid number in line:", line.strip()) #Error Message

        f.close()   #  Closing file

    except FileNotFoundError:  #Exception when file does not exixt
        print("File not found!")
        return None

    except Exception as e: # for unexpected errors
        print("Error reading file:", e)
        return None

    return data  #sends dictionary back to main progem
