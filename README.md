Instructions

This program analyzes sales team, product master and sales data to generate two reports.
	1) A team report, which breaks down sales by team.
	2) a product report, which breaks down sales by products.

Definitions:
	1) The Team Map file is a csv file with the following headers: TeamId, Name
		-Name referes to Team Name
	2) The Product Master file is a csv file with the following headers: ProductId, Name, Price, LotSize
		-Name references the products full name
		-Price is a floating point
		-LotSize defines how many products are in a single lot
	3) The Sales file is a csv file with the following headers: SaleId, ProductId, TeamId, Quantity, Discount
		-TeamId references the team that sold the product
		-Quantity is the amount sold in lots
		-Discount is expressed as a floating point percent (eg. 1.25 = 1.25%) for any applicable discount rate applied to the sale
	4) The Team Report is a csv file with the following headers: Team, GrossRevenue
		-It is sorted in descending order by GrossRevenue
	5) The Product Report is a csv file with the following headers: Name, GrossRevenue, TotalUnits, DiscountCost
		-DiscountCost represents the net revenue "lost" as a result of the discount. For instance, a 10% discount on a $100 item would produce a discount cost of $10
		-This file is also sorted in descending order by GrossRevenue
1. Navigate to the file directory containing report.py
2. Either move report.py to a directory containing a 
2. Open a terminal window, and execute the follow command: Note all 5 options are required (Where it says "path to X", please provide the full filepath to the file. For the team-report and product-report, provide the path of where you wish the file to be, it does not have to be a real file)
	> python3 report.py -t [path to Team Map CSV] -p [path to Product Master CSV] -s [path to Sales CSV] --team-report=[Path to Team Report CSV] --product-report=[Path to Product Report CSV]
3. View Calculations produced in the Team Report and Product Report CSV documents.
