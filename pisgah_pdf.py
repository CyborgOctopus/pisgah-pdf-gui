#!/usr/bin/env python3
# 
# Takes two PDF files as input (Lexis PDF report and CIPRS PDF report provided by 
# legal department)
# .
# Outputs one text file, which has a list of all case numbers in the Lexis PDF report that are 
# NOT in the CIPRS PDF report.
#
# Note: As per client, using the last 6 characters of the case number identifies the case
# number, even though the other characters might be coded differently.

# external libraries
import fitz
from datetime import datetime

# print (Lexis_pdf_document + " has " + str(doc.pageCount+1) + " pages")


# Lexis PDF parsing
def get_lexis_case_numbers(doc):
    lexis_case_number_list = []

    for page_number in range(0, doc.pageCount):
        page = doc.loadPage(page_number)
        page_text = page.getText("text")
        keyword = "Case Number:"
        case_number_split = page_text.split(keyword)
        for case_number_plus in case_number_split[1:]:
            case_number = case_number_plus.split("\n") # case number between newlines
            lexis_case_number_list.append(case_number[1])

    return lexis_case_number_list

# print (CIPRS_pdf_document + " has " + str(doc.pageCount+1) + " pages")


# CIPRS PDF parsing
def get_ciprs_case_numbers(doc):
    ciprs_case_number_list = []

    for page_number in range(0,doc.pageCount):
        page = doc.loadPage(page_number)
        page_text = page.getText("text")
        keyword = "Court Case:"
        case_number_split = page_text.split(keyword)
        for case_number_plus in case_number_split[1:]:
            case_number = case_number_plus.split("\n")[0].strip() # case number btwn space and newline
            ciprs_case_number_list.append(case_number)
    return ciprs_case_number_list


# compare the case numbers based on last 6 digits
def get_lexis_cases_not_in_ciprs(lexis_case_number_list, ciprs_case_number_list):
    lexis_cases_not_found = []
    lexis_cases_six_digits_not_found = []
    for lexis_case_number in lexis_case_number_list:
        lexis_case_six_digit = lexis_case_number[-6:]
        found_match = False
        for ciprs_case_number in ciprs_case_number_list:
            if lexis_case_six_digit == ciprs_case_number[-6:]:
                found_match = True
        if found_match == False:
            # only report if new case number (based on last-6-digits)
            if lexis_case_six_digit not in lexis_cases_six_digits_not_found:
                lexis_cases_six_digits_not_found.append(lexis_case_six_digit)
                # only report if new case number (full case number)
                if lexis_case_number not in lexis_cases_not_found:
                    lexis_cases_not_found.append(lexis_case_number)
    return lexis_cases_not_found


# write the case numbers found in Lexis but not in CIPRS
def file_comparison(lexis_file_path, ciprs_file_path, out_file_path):
    lexis_doc = fitz.open(lexis_file_path)
    ciprs_doc = fitz.open(ciprs_file_path)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    lexis_case_numbers = get_lexis_case_numbers(lexis_doc)
    ciprs_case_numbers = get_ciprs_case_numbers(ciprs_doc)
    lexis_not_in_ciprs = get_lexis_cases_not_in_ciprs(lexis_case_numbers, ciprs_case_numbers)
    with open(out_file_path, 'w') as f:
        f.write("Comparing " + lexis_file_path + " and " + ciprs_file_path + " on " + dt_string + "\n")
        for lexis_case_number in lexis_not_in_ciprs:
            f.write("Lexis case " + lexis_case_number + " not in CIPRS\n")
