#-*- coding: utf-8 -*-
"""
Created on Sat May 28 15:15:37 2022

@author: shresht
"""
import pandas as pd
from flipkart_scraper import flipkart_driver
from amazon_scraper import amazon_driver


def print_sortby_menu():
    print("Select 'Sort by' preference- ")
    print("[1] Relevance/Featured (Default)")
    print("[2] Popularity/Avg. Customer Review")
    print("[3] Price: Low to High")
    print("[4] Price: High to Low")
    print("[5] Newest Arrival")

def get_input():
    search_term = ''
    while len(search_term) <= 0 :
        search_term = input("Enter search terms: ")
    try:
        num_prod = int(input("Enter number of products to be scraped (Max 50) : "))
    except:
        print("Invalid Input. Using default value of: 10")
        num_prod = 10
    print("\n")
    sort_by = ''
    while sort_by not in ["1","2","3","4","5"]:
        print_sortby_menu()
        sort_by = input("Enter selection Number:")
        print("\n")
        if sort_by not in ["1","2","3","4","5"]:
            print("Please select a valid option.")
    pin_code = input("Enter pincode: ")
    if len(pin_code)<6:
        print("Invalid pincode. Using default value: 400072")
        pin_code = "400072"
    print("\n")
    try:
        price_min = int(input("Enter min price (if any): "))
    except:
        print("Invalid Input. Using default values: No min price")
        price_min = 0
    try:
        price_max = int(input("Enter max price (if any): "))
    except:
        print("Invalid Input. Using default values: No max price")
        price_max = -1
    return search_term,num_prod,sort_by,price_min,price_max,pin_code



if __name__ == "__main__":
    search_term,num_prod,sort_by,price_min,price_max,pin_code = get_input()                  # Get Input from user
    prod_name,prod_link,source,price,category,model_number = flipkart_driver(search_term,num_prod,sort_by,price_min,price_max,pin_code)    # Scrape Flipkart
    names, links, sourcea, prices,categorya, model = amazon_driver(search_term,num_prod,sort_by,price_min,price_max,pin_code)              # Scrape Amazon
    prod_name = prod_name + names   # combine data recieved from Amazon and Flipkart
    prod_link = prod_link + links
    source = source + sourcea
    price = price + prices
    category = category + categorya
    model_number = model_number + model
    output = pd.DataFrame(
                {
                'Names':prod_name,
                'Source': source,
                'Price': price,
                'Category':category,
                'Model no./Unique No.':model_number
                })
    writer = pd.ExcelWriter('Results.xlsx', engine='xlsxwriter')
    output.to_excel(writer,sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    colidx=1
    for rowidx,i in output.iterrows():
        worksheet.write_url(rowidx+1, colidx, prod_link[rowidx],string=i['Names'])          # Add hyperlink to Name column
    writer.save()
    
    
    
    