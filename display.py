def display(data):

    '''
    Displays the medicine data and records in a formatted way.

    Data is the dictionary where:
    Key: medicine ID
    value: list containing [name, brand, stock, unit_price, strip_price, per_strip]

    ID, Name, Brand, and Stock are displayed in a tabular format.

    Parameters:
        data (dict): Dictionary containing medicine records

    Returns:
        None
    '''

    print("\n" + "=" * 90) #prints 90 dashes to create a table like border
    print(f"{'MEDICINE LIST':^90}")
    print("=" * 90)
    print(f"{'ID':<5}{'Name':<20}{'Brand':<20}{'Stock':<10}{'Tablet Rs':<12}{'Strip Rs':<12}{'Per Strip':<10}")  #Printing the headings in formatted way
    print("-" * 90)  #prints 90 dashes to create a table like border

    for med_id, details in data.items(): #Loops through dictionary
        name, brand, stock, tab_price, strip_price, per_strip = details
        print(f"{med_id:<5}{name:<20}{brand:<20}{stock:<10}{tab_price:<12}{strip_price:<12}{per_strip:<10}")#prints data in formatted order

    print("=" * 90)
