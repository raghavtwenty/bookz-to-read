"""
This program clears duplicates and filters out contents in pdf
Designed and Developed by: Raghava, KV CBE.
Author: Raghava | GitHub: @raghavtwenty
Created On: 19 July 2021
Last Updated: 10 May 2024
"""

# -----------------------------------------------------------------------------
# importing required modules

import PyPDF2
import tkinter as tk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tkinter import filedialog
from fpdf import FPDF


# -----------------------------------------------------------------------------
# creating data types

Extracted_PDF_List = list()
Seperated_Numbers_List = list()
Removed_FSpace_List = list()
Title_Case_List = list()
Cleaned_List = list()
Similarity_List = list()
Sorted_Similarity_List = list()
Final_List = list()

New_Sorted_Dictionary = dict()


# -----------------------------------------------------------------------------
# extracting pdf file


def Extract_PDF():

    file_type_import = [("Pdf Document", "*.pdf")]
    file_pdf_import = filedialog.askopenfile(
        initialfile="", filetypes=file_type_import, defaultextension=file_type_import
    )
    pdf_file_name = file_pdf_import.name
    with open(pdf_file_name, "rb") as pdf_file:

        # creating a pdf reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # page count
        total_pages = pdf_reader.numPages

        # printing number of pages in pdf file
        print(f"Total number of pages: {total_pages}.")

        # creating a page object
        for total_pages in range(total_pages):
            page_content = pdf_reader.getPage(total_pages)

            # extracting Text_Box from page
            contents = page_content.extract()
            print(contents)
            Removed_Slash_N = contents.split("\n")
            Extracted_PDF_List.extend(Removed_Slash_N)

        # closing the pdf file object
        pdf_file.close()


# -----------------------------------------------------------------------------
# processing pdf


# splitting numbers and string in 'Extracted_PDF_List'
def Splitting_NandS():
    global Seperated_Numbers_List

    for Extract in Extracted_PDF_List:
        Numbers_Split = Extract.split(".")
        Seperated_Numbers_List.extend(Numbers_Split)

    # clear 'Extracted_PDF_List', as no more it is required
    Extracted_PDF_List.clear()


# -----------------------------------------------------------------------------
# remove numbers and front spaces


def Remove_Numbers_and_Front_Spaces():
    global Removed_FSpace_List

    # remove numbers in 'Seperated_Numbers_List'
    for Content in Seperated_Numbers_List:
        try:
            int(Content)
        except:
            Extracted_PDF_List.append(Content)

    # remove front spaces in 'Extracted_PDF_list'
    for Front_Spaces in Extracted_PDF_List:
        Removed_FSpace = Front_Spaces.strip()
        if not len(Removed_FSpace) == 0:
            Removed_FSpace_List.append(Removed_FSpace)


# -----------------------------------------------------------------------------
# title case, sort and clean duplicates


def TitleCase_and_Clean():
    global Cleaned_List

    # title case contents in 'Removed_FSpace_List'
    for String in Removed_FSpace_List:
        Titled = String.title()
        Title_Case_List.append(Titled)

    # sort 'Title_Case_List'
    Sorted_List = sorted(Title_Case_List)

    # clean 'Sorted_List'
    for Clean in Sorted_List:
        if Clean not in Cleaned_List:
            Cleaned_List.append(Clean)


# -----------------------------------------------------------------------------
# save final pdf
def Save_PDF():

    file_type_import = [("Pdf Document", "*.pdf")]
    file_location = filedialog.asksaveasfile(
        initialfile="", filetypes=file_type_import, defaultextension=file_type_import
    )
    # pdf file
    file_location_name = file_location.name  # file.name to remove ioText_Boxwrapper
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", "", size=15)

    for Print_pdf in range(len(Final_List)):
        pdf.cell(
            200, 10, txt=f"{Print_pdf}. {Final_List[Print_pdf]}\n", ln=10, align="L"
        )
    pdf.output(file_location_name)


# -----------------------------------------------------------------------------
# calling functions

Extract_PDF()
Splitting_NandS()
Remove_Numbers_and_Front_Spaces()
TitleCase_and_Clean()


# -----------------------------------------------------------------------------
# appending 'Cleaned_List'
print(Cleaned_List)
for Content in range(len(Cleaned_List)):
    New_Sorted_Dictionary[Content] = Cleaned_List[Content]

    # finding similarities in 'Cleaned_List'

    # initinalizing X and Y
    X = Cleaned_List[Content]
    try:
        Y = Cleaned_List[Content + 1]
    except:
        pass

    # tokenization
    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

    # sw contains the list of stopwords
    sw = stopwords.words("english")
    l1 = []
    l2 = []

    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
        cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

    # append similarities to the list
    Similarity = f"Book No. {Content}  and {Content+1} are matching with a Probabilty of: {cosine:.2}"
    Similarity_List.append(Similarity)


# -----------------------------------------------------------------------------
# printing out 'New_Sorted_Dictionary'

for B_NO, B_NAME in New_Sorted_Dictionary.items():
    print(f"{B_NO}. {B_NAME}")

print("-" * 30)
Similarity_List.pop(-1)


# -----------------------------------------------------------------------------
# sort out contents having similarity above 0.6

for Similarities in Similarity_List:
    Split_Similarities = Similarities.split(":")
    if float(Split_Similarities[-1]) >= 0.6:
        Sorted_Similarity_List.append(Similarities)

# iterate 'Sorted_Similarity_List' for printing out
print(f"TOTAL DUPLICATES: {len(Sorted_Similarity_List)}")
for AB0_6 in Sorted_Similarity_List:
    print(AB0_6)


# -----------------------------------------------------------------------------
if len(Sorted_Similarity_List) > 0:
    ask_to_del = str(input("Do you want to delete all above duplicates (y/n):")).lower()
    TempList = []

    if ask_to_del in ["y", "yes"]:

        # split out the repeating book number in 'Sorted_Similarity_List'
        for Content_SSL in Sorted_Similarity_List:
            Splitting_SSL = Content_SSL.split()
            TempList.append(int(Splitting_SSL[2]))

        # delete duplicates in 'New_Sorted_Dictionary'
        for Content_TempList in TempList:
            if int(Content_TempList) in New_Sorted_Dictionary:
                del New_Sorted_Dictionary[int(Content_TempList)]

        # append new items to 'Final_List'
        for Content_NSD in New_Sorted_Dictionary.values():
            Final_List.append(Content_NSD)

        # final show
        print("=" * 40)
        for Final in range(len(Final_List)):
            print(f"{Final}. {Final_List[Final]}")

        print("Duplicates Removed")

        # save pdf
        Save_PDF()

    elif ask_to_del in ["n", "no"]:
        print("NO CHANGES HAS BEEN MADE.")
    else:
        print("closed.")
else:
    print("It looks fine...")

# -----------------------------------------------------------------------------
