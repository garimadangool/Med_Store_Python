def write_data(file, data):
    
    '''
    Writes medicine data from the dictionery into the file in CVS format.

    The dictionery must contain list with:
    name, company, stock, unit_price, strip_price, per_strip

    If the updated file already exist it is overwritten

    Parameter:
        file (str): The name of the file to write data into
        data (dict): Dictionary containing medicine records

    Returns:
        None
    '''
    
    try:
        f = open(file, "w")   # Opening the file

        for value in data.values(): # loop through dictionary values
            f.write(f"{value[0]},{value[1]},{value[2]},{value[3]},{value[4]},{value[5]}\n") # Converting list into String

        f.close()  # Closing the file

    except Exception as e: #Chatches Error
        print("Error writing file:", e)
