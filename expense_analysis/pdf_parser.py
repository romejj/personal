#!/usr/bin/env python

import pdfplumber
import pprint
import os
import re
import csv
import pandas as pd
from pathlib import Path

def main():
    dbs_source_dir = Path("/Users/jeromeko/Desktop/2020_Bank_Statements/DBS")
    uob_source_dir = Path("/Users/jeromeko/Desktop/2020_Bank_Statements/UOB")
    dest_csv = Path("/Users/jeromeko/Desktop/2020_Bank_Statements")

    dbs_all_txns = []
    uob_all_txns = []

    for folder, subfolder, pdf_files in os.walk(dbs_source_dir):
        for pdf_file in pdf_files:

            with pdfplumber.open(dbs_source_dir / pdf_file) as pdf:
                for i in range(2):  # txns only extend up to 2nd page
                        page_text = pdf.pages[i].extract_text()
                        sub_total_bool, sub_total_content = contains_sub_total(pdf.pages[0].extract_text())

                        if i == 0:
                            txns_raw = txn_trimming(page_text, "NEW TRANSACTIONS JEROME KO JIA JIN")
                            dbs_all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

                        elif i == 1 and not sub_total_bool:  # if txns extend to 2nd page
                            txns_raw = txn_trimming(page_text, "2 of 3")
                            dbs_all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

    for folder, subfolder, pdf_files in os.walk(uob_source_dir):
        for pdf_file in pdf_files:

            with pdfplumber.open(uob_source_dir / pdf_file) as pdf:
                for i in range(2):  # txns only extend up to 2nd page
                        page_text = pdf.pages[i].extract_text()
                        sub_total_bool, sub_total_content = contains_sub_total(pdf.pages[0].extract_text())

                        if i == 0:
                            txns_raw = txn_trimming(page_text, "PREVIOUS BALANCE")
                            uob_all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

                        elif i == 1 and not sub_total_bool:  # if txns extend to 2nd page
                            txns_raw = txn_trimming(page_text, "Date Date SGD")
                            uob_all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

    for monthly_txns in uob_all_txns:
        for txn in monthly_txns:
            del txn[0:2]  # remove post dates

    all_txns = dbs_all_txns.copy()
    all_txns.extend(uob_all_txns)

    # Represent txns according to dates, desc and amt
    categorized_txns = [{"Date": " ".join(txn[0:2]), "Txn Desc": " ".join(txn[2:len(txn)-1]), "Amt": txn[-1]}
                        for monthly_txns in all_txns 
                        for txn in monthly_txns]

    # Load into dataframe for further manipulation
    df_categorized_txns = pd.DataFrame(categorized_txns)

    # Format date column
    df_categorized_txns["Date"] = df_categorized_txns["Date"] + " 2020"

    # Categorizing txns
    df_categorized_txns["Category"] = df_categorized_txns.apply(categorize_txns, axis=1)

    # Write into csv
    # df_categorized_txns.to_csv(dest_csv / "2020 transactions.csv")
    df_categorized_txns.to_csv(dest_csv / "2020 transactions test.csv")

# All functions placed at the end for readability
def filter_legitimate_txns(txns):
    txns_split = txns.split("\n")
    txns_split_no_ref = [txn for txn in txns_split if "Ref No." not in txn]  # to cater for UOB txns
    txns_double_split = [txn.split() for txn in txns_split_no_ref]
    
    return [txn for txn in txns_double_split if len(txn) >= 4]   # Length of at least 4 (for dates, txn desc and amt)

def contains_sub_total(page):
    sub_total_regex = re.compile("SUB.TOTAL")

    if sub_total_regex.search(page):
        return True, sub_total_regex.search(page).group()
        
    else:
        return False, None

def txn_trimming(page_text, s):
    txns_raw = page_text.partition(s)[2]
    
    sub_total_bool, sub_total_content = contains_sub_total(txns_raw)
    
    if sub_total_bool:
        return txns_raw.partition(sub_total_content)[0]
        
    else:
        return txns_raw.partition("Pleasenote")[0]  # doesn't matter if statement is DBS as result is the same

def process_txn_amt(txns):
    for txn in txns:
        while not txn[-1].replace(".","",1).replace(",","",1).isdigit() and not "CR" in txn[-1]:  
            txn.pop(-1)  # remove if last item in each txn is not an amt
    
        if "CR" in txn[-1]:  # if amt contains CR
            txn[-1] = txn[-1].replace("CR","",1)  # remove CR
            txn[-1] = "-" + txn[-1]  # and reverse sign
            
    return txns

def categorize_txns(s):
    shopping = re.compile(r'''.*Shopee(pay)?.*
                        |.*Lazada.*
                        |.*Zalora.*
                        |.*Uniqlo.*
                        |.*Asos.*
                        |.*Ghbass.*
                        |.*Decathlon.*
                        |.*Amazon.*
                        |.*Watson.*
                        |.*Guardian.*''', re.I | re.VERBOSE)
    utilities = re.compile(r".*Liberty Wireless.*|.*Gomo.*", re.I)
    holiday = re.compile(r".*Agoda*.|.*Scoot.*|.*Hotel.*", re.I)
    grooming = re.compile(".*Sultans of shave.*", re.I)
    entertainment = re.compile(r".*GV.*|.*Shaw.*", re.I)
    others = re.compile(r".* Fee.*|.*Charge.*|.*Interest.*|.*Bank.*|.*Rebate.*", re.I)

    if shopping.search(s["Txn Desc"]):  # None if there's no match
        return "Shopping"
    
    elif utilities.search(s["Txn Desc"]):
        return "Utilities"
    
    elif holiday.search(s["Txn Desc"]):
        return "Holiday"
    
    elif grooming.search(s["Txn Desc"]):
        return "Grooming"
    
    elif entertainment.search(s["Txn Desc"]):
        return "Entertainment"
    
    elif others.search(s["Txn Desc"]):
        return "Others"
    
    elif s["Date"] == "27 JUN 2020":
        return "Birthday"
    
    elif s["Date"] == "19 MAR 2020":
        return "Anniversary"
    
    else:
        return "Food"

if __name__ == '__main__':
    main()