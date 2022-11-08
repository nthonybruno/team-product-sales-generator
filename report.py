# Python version: 3.1
# Description: Reads from 3 input files and produces 2 output files, the names of each must be provided as input.
# Constraints: Built-in python packages only.

# Required imports (all are built-in Python packages)
import sys
import getopt
import csv
import os

#Usage message that is printed for incorrect command structuring
usage = "Usage: python report.py -t <path to Team Map CSV file> -p <Path to Product Master CSV file> -s <Path to Sales CSV file> --team-report=<Desired output path to Team Report CSV file> --product-report=<Desired output path to Product Report CSV file>\n"

# A function to parse the CSV file and extract it's data into list format so it can be manipulated
def csv_parser(filepath, hasHeader):
    ret_object = []
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        if hasHeader:
            next(reader,None)
        for row in reader:
            ret_object.append(row)
    return ret_object

# A function to validate that all input arguements are indeed CSVs.
def validate(list_of_files):
    for file in list_of_files:
        if os.path.isfile(file):
            try:
                delim = file.split(".")
                if delim[1] != "csv":
                    print("All arguement values must be in CSV file format")
                    print(usage)
                    return False
            except:
                    print("All arguement values must be in CSV file format")
                    print(usage)
                    return False
        else:
            print(f"Error: File {file} not found.\n")
            return False
    return True

# A function to parse the command executed to make sure all 5 flags and file paths have been included. Returns a list of the 5 files if the command executed is valid
def input_parse(command_line_arguements):
    arg_count = 0
    try:
        opts, args = getopt.getopt(command_line_arguements,"t:p:s:", ["team-report=","product-report="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-t"):
            team_map_file = arg
            arg_count+=1
        elif opt in ("-p"):
            product_master_file = arg
            arg_count+=1
        elif opt in ("-s"):
            sales_file = arg
            arg_count+=1
        elif opt in ("--team-report"):
            team_report_output_file = arg
            arg_count+=1
        elif opt in ("--product-report"):
            product_report_output_file =arg
            arg_count+=1
    
    if arg_count != 5:
        print("Incomplete number of arguements, missing a total of " + str(5-arg_count))
        print(usage)
        return 1
    return [team_map_file, product_master_file, sales_file, team_report_output_file, product_report_output_file] 

# A function to match the ProductId of a sale to it's Price and LotSize in the product Master document.
def sale_matcher(productId, productMaster):
    ret_object = []
    for product in productMaster:
        if product[0] == productId:
            ret_object.append(product[2])
            ret_object.append(product[3])
    if len(ret_object) < 1:
        return -1
    return ret_object

if __name__ == '__main__':
    print("") # Increase Readability
    
    # Step 1, parse input, extract filenames
    input_files = input_parse(sys.argv[1:])

    # Step 2, validate input
    if not validate(input_files):
        sys.exit(1)
    
    # Step 3, Extract input from each file
    team_map_data = csv_parser(input_files[0], True) # Headers: TeamId, Name
    product_master_data = csv_parser(input_files[1], False) # Headers: ProductId, Name, Price, LotSize
    sales_data = csv_parser(input_files[2], False) #Headers: SaleId, ProductId, TeamId, Quantity, Discount

    # Step 4, manipulate the data
    number_of_teams = len(team_map_data)
    total_gross_revenues = [0 for i in range(number_of_teams)] # Array structure where the index represents the TeamId - 1 found in TeamMap.csv (ie, based on the example data Team 1 (Fluffy Bunnies) gross revenue is stored at the 0th index.)

    # 4.1 Initialize a data structure to store product report information for any number of products. Contains product name, gross revenue, total units sold and discount cost
    number_of_products = len(product_master_data)
    product_report = [["",0,0,0] for i in range(number_of_products)]

    # 4.2 Calculate total gross revenue per team
    for sale in sales_data:
        total_gross_revenues_index = int(sale[2]) - 1

        if total_gross_revenues_index < len(total_gross_revenues): #If this is not satisified, it means the TeamId is not referenced by the TeamMap.csv manifest
            # Get ProductId from the sale, look up the Price & LotSize in product_master_data, and multiply it by the quantity. Gross revenue not reduced by discounts
            productPriceAndLotSize = sale_matcher(sale[1], product_master_data)
            if productPriceAndLotSize == -1:
                print("Error, Could not find the ProductId referenced in a sale record in the Product Master CSV")
                sys.exit(1)

            revenue = float(productPriceAndLotSize[0]) * (int(productPriceAndLotSize[1]) * int(sale[3]))
            total_gross_revenues[total_gross_revenues_index] += revenue

        # 4.2.1: Calculate product report
            # Each Line summarizes the sales of a single product: Name, GrossRevenue, TotalUnits, DiscountCost
            # Logic: Loop over sales, reference product master to get price and lotsize
        productPriceAndLotSize = sale_matcher(sale[1], product_master_data)
        if productPriceAndLotSize == -1:
            print("Error, Could not find the ProductId referenced in a sale record in the Product Master CSV")
            sys.exit(1)
        #Depending on productId, update that index with appropriate information
        product_ID_Of_Current_Sale = int(sale[1])

        if product_ID_Of_Current_Sale-1 < len(product_master_data):
            product_report[product_ID_Of_Current_Sale-1][0] = product_master_data[product_ID_Of_Current_Sale-1][1] # 0 index is name of product, 1 is gross revenue, 2 is total units, 3 is discount cost.

            revenue = float(productPriceAndLotSize[0]) * (int(productPriceAndLotSize[1]) * int(sale[3]))

            product_report[product_ID_Of_Current_Sale-1][1] = product_report[product_ID_Of_Current_Sale-1][1] + revenue

            product_report[product_ID_Of_Current_Sale-1][2] = product_report[product_ID_Of_Current_Sale-1][2] + int(sale[3])

            # Calculating Discount Cost
                # Calculate total net discount price, and subtract that from the products gross revenue. The difference is the discount cost.
                # If a product did $7500 in sales, but after discounts only took in $6900, then the discount cost is $600.
            try:
                discount_price = revenue - (revenue * (float(sale[4])/100))
            except:
                discount_price = 0
            
            #print(discount_price)
            discount_cost = revenue - discount_price
            product_report[product_ID_Of_Current_Sale-1][3] = product_report[product_ID_Of_Current_Sale-1][3] + discount_cost
        # If a product did not have any sales, this will catch the empty record and add the name to the product_report object to include products w/ no sales in the product report
        i = 0
        for record in product_report:
            if record[0] == "":
                record[0] = product_master_data[i][1]
            i+=1

    # Step 5 Return two output files: Team Report and Product Report

    # 5.1 Output total gross revenues by team

    # 5.1.1 Lookup team
    team_report = []
    for i in range(0,len(total_gross_revenues)):
        team_name = team_map_data[i][1]
        team_report.append([team_name,total_gross_revenues[i]])
    
    # 5.1.2 Sort in descending order
    sorted_team_report = sorted(team_report, key=lambda x: int(x[1]), reverse=True)
    
    # 5.1.3 Write to CSV
    headers = ['Team','GrossRevenue']
    with open(input_files[3], 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for entry in sorted_team_report:
            writer.writerow(entry,)

    # 5.2 Output Product Report

    # 5.2.1 Sort in descending order
    sorted_product_report = sorted(product_report, key=lambda x: int(x[1]), reverse=True)

    # 5.2.2 Write to CSV
    headers = ["Name" , "GrossRevenue", "TotalUnits", "DiscountCost"]
    with open(input_files[4], 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for entry in sorted_product_report:
            writer.writerow(entry)

    print(f"Successfully calculated the Team Report and Product Report, output files to {input_files[3]} and {input_files[4]}, respectively.")
    print("") # Increase Readability
