import datetime

def sell_medicine(data):
    '''
    Processes medicine transactions to customer
    
    This function  including customer name,medicine ID selection,
    quantity validation, discount calculation, stock updates,
    and invoice generation.
    
    Parameters:
    data (dict): Medicine database with structure {med_id: [name, brand, stock, 
                 tab_price, strip_price, per_strip]}
    
    Returns:
    None: Prints bill and generates invoice file
    
    Discount Rules:
    - Tablets: 5% discount when quantity >= 2 strips worth (qty >= 2 * per_strip)
    - Strips: 5% discount when quantity >= 2 strips
    '''
    
    cart = []  # Stores sale items: [name, brand, unit_name, qty, total, discount]
    grand_total = 0  
    
    print("\n--- SALE SECTION ---")
    customer_name = input("Enter customer name: ")
    
    while True:
        try:
            print("\n" + "-" * 50)
            
            # VALID ID - Loop until valid medicine ID is entered
            while True:
                try:
                    med_id = int(input("Enter medicine ID: "))
                    if med_id in data:
                        break
                    print("Invalid ID! Try again.")
                except ValueError:
                    print("Enter a valid number!")
            
            # VALID UNIT - Loop until 't' or 's' is entered
            while True:
                unit = input("Tablet or Strip (t/s): ").lower()
                if unit in ["t", "s"]:
                    break
                print("Invalid input!")
            
            # VALID QTY - Loop until positive quantity is entered
            while True:
                try:
                    qty = int(input("Enter quantity: "))
                    if qty > 0:
                        break
                    print("Quantity must be greater than 0!")
                except ValueError:
                    print("Enter a number!")
            
            # Extracts medicine details from database
            name, brand, stock, tab_price, strip_price, per_strip = data[med_id]
            discount = 0
            
            #  Tablet purchase
            if unit == "t":
                # Checks if enough stock id available
                while qty > stock:
                    print("Not enough stock!")
                    qty = int(input("Enter quantity: "))
                
                # Calculate total price
                total = qty * tab_price
                
                # Apply 5% discount for (2 or more strips )
                if qty >= (2 * per_strip):
                    discount = total * 0.05
                    total = total - discount
                
                # Update stock 
                data[med_id][2] -= qty
                unit_name = "Tablet"
            
            #Strip purchase
            else:
                # Calculate total tablets needed
                tablets_needed = qty * per_strip
                
                # Checks if enough stock is available
                while tablets_needed > stock:
                    print("Not enough stock!")
                    qty = int(input("Enter strips: "))
                    tablets_needed = qty * per_strip
                
                # Calculate total price
                total = qty * strip_price
                
                # Apply 5% discount for 2 or more strips
                if qty >= 2:
                    discount = total * 0.05
                    total -= discount
                
                # Update stock 
                data[med_id][2] -= tablets_needed
                unit_name = "Strip"
            
            # Displays item 
            print("-" * 50)
            print(f"Item Added | Total: Rs {total:.2f}")
            print(f"Remaining Stock: {data[med_id][2]}")
            
            # Add item to cart
            cart.append([name, brand, unit_name, qty, total, discount])
            grand_total += total
            
            # Ask if user wants to add more items
            more = input("\nAdd more? (y/n): ").lower()
            if more != "y":
                break
                
        except Exception:
            print("Something went wrong. Try again.")
    
    # FINAL BILL - Displays bill summary
    print("\n" + "=" * 70)
    print(f"{'FINAL BILL':^70}")
    print("=" * 70)
    
    # Prints bill header
    print(f"{'Medicine':<20}{'Unit':<10}{'Qty':<10}{'Total (Rs)':<15}")
    print("-" * 70)
    
    # Prints each cart item
    for item in cart:
        print(f"{item[0]:<20}{item[2]:<10}{item[3]:<10}{item[4]:<15.2f}")
    
    # Prints grand total
    print("-" * 70)
    print(f"{'GRAND TOTAL':<40} Rs {grand_total:.2f}")
    print("=" * 70)
    
    # Generate sales invoice file
    generate_sale_invoice(cart, customer_name, grand_total)


def restock_medicine(data):
    '''
    This function restocks medicines for vendors
    
    This function asks for vendors information, medicine ID selectin for  adding new stock to existing medicines,
    updates inventory quantities, and generates a restock invoice.
    
    Parameters:
    data (dict): Medicine database with structure {med_id: [name, brand, stock, 
                 tab_price, strip_price, per_strip]}
    
    Returns:
    None: Updates stock and generates restock invoice file
    '''
    
    print("\n--- RESTOCK SECTION ---")
    vendor_name = input("Enter vendor name: ")
    
    while True:
        try:
            print("\n" + "-" * 50)
            
            # VALID MEDICINE ID - Loop until existing ID is entered
            while True:
                try:
                    med_id = int(input("Enter medicine ID: "))
                    if med_id in data:
                        break
                    print("Invalid ID!")
                except ValueError:
                    print("Enter number!")
            
            # VALID QUANTITY - Loop until positive quantity is entered
            while True:
                try:
                    qty = int(input("Enter quantity: "))
                    if qty > 0:
                        break
                    print("Must be > 0")
                except ValueError:
                    print("Enter number!")
            
            # Store stock before update
            before = data[med_id][2]
            
            # Update stock (add new quantity)
            data[med_id][2] += qty
            
            # Store stock after update
            after = data[med_id][2]
            
            # Displays restock confirmation
            print("-" * 50)
            print("Restock Successful")
            print(f"Before: {before} | Added: {qty} | After: {after}")
            
            # Prepare cart data for invoice
            cart = [[data[med_id][0], data[med_id][1], qty, before, after]]
            
            # Generate restock invoice
            generate_restock_invoice(cart, vendor_name, qty)
            
            break  # Exit after successful restock
            
        except Exception:
            print("Something went wrong.")


def generate_sale_invoice(cart, customer_name, grand_total):
    '''
    Generate a detailed sales invoice in a file.
    
    Creates a formatted text file containing complete sale information including
    customer bname, medicine information,quantities, prices, discount and totals. 
    =
    Parameters:
    cart (list): List of sale items, each containing [name, brand, unit, qty, total, discount]
    customer_name (str): Name of the customer
    grand_total (float): Total bill amount after all discounts
    
    Returns:
    None: Creates a timestamped invoice file in the current directory
    '''
    
    try:
        # Get current timestamp for invoice
        now = datetime.datetime.now()
        
        # Format date and time for display
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%I:%M:%S %p")
        
        # Create unique filename using timestamp
        timestamp = now.strftime("%Y%m%d_%I%M%S")
        filename = f"invoice_sale_{timestamp}.txt"
        
        # Write invoice to file
        with open(filename, "w") as f:
            
            # Company header
            f.write("=" * 100 + "\n")
            f.write(f"{'MEDSTORE PVT. LTD.':^100}\n")
            f.write("=" * 100 + "\n\n")
            
            # Invoice title
            f.write(f"{'SALE INVOICE':^100}\n\n")
            
            # Customer and transaction details
            f.write(f"{'Date':<15}: {date}\n")
            f.write(f"{'Time':<15}: {time}\n")
            f.write(f"{'Customer Name':<15}: {customer_name}\n\n")
            
            # Invoice table header
            f.write("-" * 100 + "\n")
            f.write(
                f"{'Medicine':<20}"
                f"{'Brand':<18}"
                f"{'Type':<10}"
                f"{'Qty':<8}"
                f"{'Price'}\n"
            )
            f.write("-" * 100 + "\n")
            
            # Calculate running totals
            subtotal = 0
            total_discount = 0
            
            # Process each item in cart
            for item in cart:
                name, brand, unit, qty, total, discount = item
                
                # Calculate original price before discount
                original_price = total + discount
                
                # Update running totals
                subtotal += original_price
                total_discount += discount
                
                # Write main medicine line
                f.write(
                    f"{name:<20}"
                    f"{brand:<18}"
                    f"{unit:<10}"
                    f"{qty:<8}"
                    f"Rs {original_price:.2f}\n"
                )
                
                #writes discount line in bill 
                if discount > 0:
                    f.write(
                        f"{'':<56}"
                        f"Discount: - Rs {discount:.2f}\n"
                    )
                
                # Writes final total for this item
                f.write(
                    f"{'':<56}"
                    f"Final Total: Rs {total:.2f}\n"
                )
                
                f.write("-" * 100 + "\n")
            
            # Summary section with totals
            f.write("\n")
            f.write(f"{'Subtotal':<75}Rs {subtotal:.2f}\n")
            f.write(f"{'Total Discount':<75}Rs {total_discount:.2f}\n")
            f.write(f"{'Grand Total':<75}Rs {grand_total:.2f}\n")
            
            # Footer with thank you message
            f.write("=" * 100 + "\n")
            f.write(f"{'Thank You For Visiting!':^100}\n")
            f.write("=" * 100 + "\n")
        
        print("Sale invoice generated:", filename)
        
    except Exception as e:
        print("Error generating sale invoice:", e)


def generate_restock_invoice(cart, vendor_name, total_quantity):
    '''
    Generate a restock invoice for restocking medicines.
    
    Creates a formatted text file , a bill in a txt file including the
    medicine details, quantity added, and stock levels before/after.
    
    Parameters:
    cart (list): List containing [name, brand, qty, before, after] for restocked items
    vendor_name (str): Name of the vendor supplying the medicine
    total_quantity (int): Total quantity of medicine added
    
    Returns:
    None: Creates a timestamped restock invoice file in the current directory
    '''
    
    try:
        # Get current timestamp for invoice
        now = datetime.datetime.now()
        
        # Format date and time for display
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%I:%M:%S %p")
        
        # Create unique filename using timestamp
        timestamp = now.strftime("%Y%m%d_%I%M%S")
        filename = f"invoice_restock_{timestamp}.txt"
        
        # Write restock invoice to file
        with open(filename, "w") as f:
            
            # Company header
            f.write("=" * 70 + "\n")
            f.write(f"{'MEDSTORE PVT. LTD.':^70}\n")
            f.write("=" * 70 + "\n\n")
            
            # Invoice title
            f.write(f"{'RESTOCK INVOICE':^70}\n\n")
            
            # Vendor and transaction details
            f.write(f"{'Date':<12}: {date}\n")
            f.write(f"{'Time':<12}: {time}\n")
            f.write(f"{'Vendor':<12}: {vendor_name}\n\n")
            
            # Invoice table header
            f.write("-" * 70 + "\n")
            f.write(f"{'Medicine':<22}{'Brand':<18}{'Added':<10}{'Before':<10}{'After'}\n")
            f.write("-" * 70 + "\n")
            
            # Write each restocked item
            for item in cart:
                name, brand, qty, before, after = item
                f.write(f"{name:<22}{brand:<18}{qty:<10}{before:<10}{after}\n")
            
            # Summary section
            f.write("-" * 70 + "\n")
            f.write(f"{'TOTAL QTY ADDED':<50}{total_quantity}\n")
            
            # Footer
            f.write("=" * 70 + "\n")
            f.write(f"{'Stock Updated Successfully':^70}\n")
            f.write("=" * 70 + "\n")
        
        print("Restock invoice generated:", filename)
        
    except Exception as e:
        print("Error generating restock invoice:", e)
