#!/usr/bin/env python

import pdfplumber
import pprint
import os
import re
import csv
from pathlib import Path

def main():
    dbs_source_dir = Path("/Users/jeromeko/Desktop/2020_Bank_Statements/DBS")
    uob_source_dir = Path("/Users/jeromeko/Desktop/2020_Bank_Statements/UOB")

    all_txns = []

    for folder, subfolder, pdf_files in os.walk(dbs_source_dir):
        for pdf_file in pdf_files:

            with pdfplumber.open(dbs_source_dir / pdf_file) as pdf:
                for i in range(2):  # txns only extend up to 2nd page
                        page_text = pdf.pages[i].extract_text()
                        all_txns_in_first = contains_sub_total(pdf.pages[0].extract_text())

                        if i == 0:
                            txns_raw = txn_trimming(page_text, "NEW TRANSACTIONS JEROME KO JIA JIN")
                            all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

                        elif i == 1 and not all_txns_in_first:  # if txns extend to 2nd page
                            txns_raw = txn_trimming(page_text, "2 of 3")
                            all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

    for folder, subfolder, pdf_files in os.walk(uob_source_dir):
        for pdf_file in pdf_files:

            with pdfplumber.open(uob_source_dir / pdf_file) as pdf:
                for i in range(2):  # txns only extend up to 2nd page
                        page_text = pdf.pages[i].extract_text()
                        all_txns_in_first = contains_sub_total(pdf.pages[0].extract_text())

                        if i == 0:
                            txns_raw = txn_trimming(page_text, "PREVIOUS BALANCE")
                            all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

                        elif i == 1 and not all_txns_in_first:  # if txns extend to 2nd page
                            txns_raw = txn_trimming(page_text, "Date Date SGD")
                            all_txns.append(process_txn_amt(filter_legitimate_txns(txns_raw)))

# All functions placed at the end for readability
def filter_legitimate_txns(txns):
    txns_split = txns.split("\n")
    txns_split_no_ref = [txn for txn in txns_split if "Ref No." not in txn] 
    txns_double_split = [txn.split() for txn in txns_split_no_ref]
    
    return [txn for txn in txns_double_split if len(txn) >= 4]

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
        return txns_raw.partition("Pleasenote")[0]

def process_txn_amt(txns):
    for txn in txns:
        while not txn[-1].replace(".","",1).replace(",","",1).isdigit() and not "CR" in txn[-1]:  
            txn.pop(-1)
    
        if "CR" in txn[-1]:
            txn[-1] = txn[-1].replace("CR","",1)
            txn[-1] = "-" + txn[-1]
            
    return txns

if __name__ == '__main__':
    main()