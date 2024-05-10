"""
Application Name: Bookz To Read
Designed and Developed by: Raghava, KV CBE.
Author: Raghava | GitHub: @raghavtwenty
Created On: 19 July 2021
Last Updated: 10 May 2024
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Importing Required Libraries

from tkinter import *
from tkinter import messagebox, ttk, filedialog
from pathlib import Path
from collections import OrderedDict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from fpdf import FPDF

import tkinter as TK
import os
import ast
import datetime


Present_Date = datetime.datetime.now()
Present_Date_TC = f"{Present_Date.day}-{Present_Date.month}-{Present_Date.year}"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create DONT-DELETE-TXT.txt File In User Home Dir


# ----- Default Books -----
def Create_New_Books_File():
    Initinal_Dict = dict()  # Writing Empty Dictionary
    with open(User_Home_Books_File, "w") as Book_File:
        Book_File.write(str(Initinal_Dict))


# ----- Default Aesthetics -----
Default_AFC = {
    "GEO": "1080x720",
    "BGC": "#AAB6FB",
    "FGC": "#031B88",
    "FSSD_Style": "Arial",
    "FSSD_Size": 25,
    "FSSD_Design": "italic",
}


def Create_New_Aesthetics_File(Default_AFC):
    with open(User_Home_Aesthetics_File, "w") as Aesthetics_File:
        Aesthetics_File.write(str(Default_AFC))


# ----- Initialize Home Directory Path -----
User_Home_Dir = Path.home() / "Bookz-To-Read"
User_Home_Books_File = f"{User_Home_Dir}/DONT-DELETE-BOOKS.txt"
User_Home_Aesthetics_File = f"{User_Home_Dir}/DONT-DELETE-AESTHETICS.txt"

# ----- Check for Dir And File -----
if User_Home_Dir.exists() == True:
    if os.path.isfile(User_Home_Books_File) == False:
        Create_New_Books_File()  # F-34
    if os.path.isfile(User_Home_Aesthetics_File) == False:
        Create_New_Aesthetics_File(Default_AFC)  # F-47

else:
    try:
        # ----- If Not Exist Create New Dir And File -----
        User_Home_Dir.mkdir()
    finally:
        Create_New_Books_File()  # F-34
        Create_New_Aesthetics_File(Default_AFC)  # F-47


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Home Window Configuration

# ----- Default Asthetics Configuration -----
global Default_Geometry
global Default_B_G
global Default_F_G
global Default_Font_Style


with open(User_Home_Aesthetics_File, "r") as Read_Aesthetics_File:
    Reader_Obj = Read_Aesthetics_File.read()  # str
    Dict_Reader_Obj = ast.literal_eval(Reader_Obj)

    Default_Geometry = Dict_Reader_Obj["GEO"]
    Default_B_G = Dict_Reader_Obj["BGC"]
    Default_F_G = Dict_Reader_Obj["FGC"]
    Default_Font_Style = (
        Dict_Reader_Obj["FSSD_Style"],
        Dict_Reader_Obj["FSSD_Size"],
        Dict_Reader_Obj["FSSD_Design"],
    )


# ----- Default Window Configuration -----
def Window_Configuration(Window_Name):

    global Window

    Window = TK.Tk()
    Window.geometry(Default_Geometry)
    Window.resizable(True, True)
    Window.title(Window_Name)
    Window["background"] = Default_B_G


Window_Configuration("Bookz To Read")  # F-96


# ------------------------------------------------------------------------------
# Functions


# save final pdf
def Save_PDF(SAVE):

    if SAVE == "SAVE":

        file_type_import = [("Pdf Document", "*.pdf")]
        file_location = filedialog.asksaveasfile(
            initialfile="",
            filetypes=file_type_import,
            defaultextension=file_type_import,
        )

        # ----- pdf file -----
        file_location_name = file_location.name  # file.name to remove ioText_Boxwrapper
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        pdf.cell(200, 10, txt="Bookz To Read\n", ln=10, align="C")
        pdf.cell(200, 10, txt=f"\nDated: {Present_Date_TC}", ln=10, align="L")
        pdf.cell(200, 10, txt="", ln=10, align="C")

        Save_Count = 1
        for Print_pdf in sorted(OFVC_List):
            pdf.cell(200, 5, txt=f"{Save_Count}. {Print_pdf}\n", ln=10, align="L")
            Save_Count += 1

        pdf.cell(200, 10, txt="", ln=10, align="C")
        pdf.cell(200, 5, txt="PDF File Exported By Bookz To Read.\n", ln=10, align="C")
        pdf.cell(
            200,
            5,
            txt="\nDesigned and Developed by: Raghava, GitHub: @raghavtwenty",
            ln=10,
            align="C",
        )
        pdf.output(file_location_name)

        Window.destroy()
        messagebox.showinfo("Saved", f"Pdf File Saved As {file_location_name}")

    else:
        Window.destroy()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Default View Window Configuration
def Default_View_Window_Configuration(Window_Name):

    global Text_Box
    global Window

    # ----- Screen -----
    Window_Configuration(Window_Name)

    # ----- apply the grid layout -----
    Window.grid_columnconfigure(0, weight=1)
    Window.grid_rowconfigure(0, weight=1)

    # ----- create the Text_Box widget -----
    Text_Box = Text(
        Window,
        height=10,
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
        wrap="none",
    )
    Text_Box.grid(row=0, column=0, sticky="nsew")

    # ----- create a scrollbar widget and set its command to the Text_Box widget -----
    scrollbar_V = ttk.Scrollbar(Window, orient="vertical", command=Text_Box.yview)
    scrollbar_V.grid(row=0, column=1, sticky="nsew")
    scrollbar_H = ttk.Scrollbar(Window, orient="horizontal", command=Text_Box.xview)
    scrollbar_H.grid(row=1, column=0, sticky="nsew")

    # ----- Communicate back to the scrollbar -----
    Text_Box["yscrollcommand"] = scrollbar_V.set
    Text_Box["xscrollcommand"] = scrollbar_H.set


# ------------------------------------------------------------------------------
# Opening File
def Opening_File_View_Content(Label_Name):

    global OFVC_List

    with open(User_Home_Books_File, "r") as Read_Books_TXT:
        Reader_Obj = Read_Books_TXT.read()  # str
        Dict_Reader_Obj = ast.literal_eval(Reader_Obj)  # str to dict using ast

        # ----- Add To List -----
        OFVC_List = list()
        if not len(Dict_Reader_Obj) == 0:
            for KEY, VALUES in Dict_Reader_Obj.items():
                OFVC_List.append(f"{KEY} --- By {VALUES[0]} --- Added on {VALUES[1]}")

        else:
            # ----- Show Error Message -----
            Window.destroy()
            messagebox.showerror(
                "File Empty", "Books File Empty. Please, Try Adding New Books."
            )

    # ----- Sort In Ascending Order And Show -----
    Count = 0  # Initial Count
    for Content_OFVC_List in sorted(OFVC_List):
        Text_Box.insert(TK.END, f"{Count+1}. {Content_OFVC_List} \n\n")
        Count += 1

    Text_Box.configure(state="disabled")

    Label(
        Window, text=" ", font=Default_Font_Style, bg=Default_B_G, fg=Default_F_G
    ).grid(row=2, column=0, sticky="nsew")

    Label(
        Window, text=Label_Name, font=Default_Font_Style, bg=Default_B_G, fg=Default_F_G
    ).grid(row=3, column=0, sticky="nsew")


# ------------------------------------------------------------------------------
# View Books
def View_Books():

    Default_View_Window_Configuration("View Books")
    Opening_File_View_Content("Do You Want To Export To PDF?")

    Button(
        Window,
        text="SAVE NOW",
        command=lambda SAVE="SAVE": Save_PDF(SAVE),
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=4, column=0, sticky="nsew")

    Button(
        Window,
        text="NOT NOW",
        command=lambda NOT_NOW="NOT_NOW": Save_PDF(NOT_NOW),
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=5, column=0, sticky="nsew")


# ------------------------------------------------------------------------------
# Sort Duplicates
def Sort_Duplicates():

    Default_View_Window_Configuration("Find Similarities")

    # ----- Opening File -----
    New_Sorted_Dictionary = dict()
    with open(User_Home_Books_File, "r+") as Read_Sort_Duplicates:
        Reader_Obj = Read_Sort_Duplicates.read()  # str
        Dict_Reader_Obj = ast.literal_eval(Reader_Obj)  # str to dict using ast
        New_Sorted_Dictionary = OrderedDict(sorted(Dict_Reader_Obj.items()))

    # ----- On Screen Show -----
    RSD_List = list()
    RSD_Count = 1
    if len(New_Sorted_Dictionary) > 1:

        # ----- Show To The User -----
        for RSD_KEY, RSD_VALUE in New_Sorted_Dictionary.items():

            Sort_Temp_Str = f"{RSD_KEY} by {RSD_VALUE[0]}"
            Text_Box.insert(TK.END, f"{RSD_Count}. {Sort_Temp_Str}\n")
            RSD_List.append(Sort_Temp_Str)
            RSD_Count += 1

    Text_Box.insert(TK.END, "\n" + "~" * 70 + "\n")
    Text_Box.insert(TK.END, "\t\t Similarities \n\n")

    # -------- Finding Similarity -------
    Similarity_List = list()
    for RSD_X_Content in range(len(RSD_List)):

        # initinalizing X and Y
        X = RSD_List[RSD_X_Content]
        for RSD_Y_Content in range(len(RSD_List)):
            Y = RSD_List[RSD_Y_Content]

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
            Similarity = f"Book No. {RSD_X_Content+1}  and {RSD_Y_Content+1} are matching with a Probabilty of: {cosine:.2}"
            Similarity_List.append(Similarity)

    Similarity_List.pop(-1)
    for Similarity_Content in Similarity_List:
        Temp_Similarity_Content = Similarity_Content.split()
        if (
            float(Temp_Similarity_Content[-1]) > 0.6
            and float(Temp_Similarity_Content[-1]) < 1.0
        ):
            Text_Box.insert(TK.END, f"{Similarity_Content}\n")

    Text_Box.configure(state="disabled")


# ------------------------------------------------------------------------------
# Add Book
def Add_a_Book():

    # ----- Submit_New_Book - Appending Into .txt File -----
    def Submit_New_Book(SubmitNewBook):
        if SubmitNewBook == "YES":

            # Arranging Book And Author Name
            Book_Name = str(Enter_Book_Name.get())
            Author_Name = str(Enter_Author_Name.get())
            Book_Name = Book_Name.strip()
            Author_Name = Author_Name.strip()
            Book_Name_TC = Book_Name.title()
            Author_Name_TC = Author_Name.title()

            if not Book_Name == "" and not Author_Name == "":

                # Opens File And Reads
                with open(User_Home_Books_File, "r") as Read_Books_TXT:
                    Reader_Obj = Read_Books_TXT.read()  # Text_Box file content str
                    Dict_Reader_Obj = ast.literal_eval(
                        Reader_Obj
                    )  # str to dict using ast

                # ----- Checks New Book With Old Book -----
                if Book_Name not in Dict_Reader_Obj:

                    # ----- Open File For Adding Book -----
                    with open(User_Home_Books_File, "w") as New_Book_Append:
                        Dict_Reader_Obj[Book_Name_TC] = [
                            Author_Name_TC,
                            Present_Date_TC,
                        ]
                        New_Book_Append.write(str(Dict_Reader_Obj))

                        Window.destroy()
                        messagebox.showinfo(
                            "Book Added", f"{Book_Name.title()}, Added to all books."
                        )

                else:
                    messagebox.showerror(
                        "Book Exist",
                        f"{Book_Name.title()}, Book Already Exist In All Books.",
                    )

            else:
                messagebox.showerror(
                    "Field Empty", "Please, Enter A Vaild Book Name And A Author Name."
                )

    Window_Configuration("Add Book")  # F - Line 87

    # ----- Book Name -----
    Label(
        Window,
        text="Enter Book Name",
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).pack(pady=5)

    # ----- Enter Book Name -----
    Enter_Book_Name = TK.Entry(Window, font=Default_Font_Style)
    Enter_Book_Name.pack(pady=5)

    # ----- Author Name -----
    Label(
        Window,
        text="Enter Author Name",
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).pack(pady=5)

    # ----- Enter Author Name -----
    Enter_Author_Name = TK.Entry(Window, font=Default_Font_Style)
    Enter_Author_Name.pack(pady=5)

    # ----- Submit_New_Book Button -----
    Button(
        Window,
        text="Submit",
        command=lambda SubmitNewBook="YES": Submit_New_Book(SubmitNewBook),
        font=("Arial", "25", "italic"),
        bg=Default_B_G,
        fg=Default_F_G,
    ).pack(pady=5)


# ------------------------------------------------------------------------------
# Mark as Read
def Mark_As_Read():

    def Completed(Mark_Read):

        # ----- Opening File -----
        with open(User_Home_Books_File, "r+") as Completed_TXT:

            # ----- Initialzation -----
            Reader_Obj = Completed_TXT.read()  # str
            Dict_Reader_Obj = ast.literal_eval(Reader_Obj)  # str to dict using ast
            BNR_GET = Book_Name_MAR.get()
            BNR_GET = BNR_GET.strip()
            BNR_TC = BNR_GET.title()

            if not len(BNR_TC) == 0:
                if BNR_TC in Dict_Reader_Obj:
                    Ret_Date_Added = Dict_Reader_Obj[BNR_TC].pop(1)
                    if not "Completed" in Ret_Date_Added:
                        Read_Date = (
                            f"{Ret_Date_Added} --- Completed On {Present_Date_TC}"
                        )
                        Dict_Reader_Obj[BNR_TC].append(Read_Date)

                        # ----- Update .txt File -----
                        with open(User_Home_Books_File, "w") as Update_Books_TXT:
                            Update_Books_TXT.write(str(Dict_Reader_Obj))

                        Window.destroy()
                        messagebox.showinfo(
                            "Completed", f"You Marked '{BNR_TC}' As Completed"
                        )

                    else:
                        messagebox.showerror(
                            "Duplication",
                            f"You Had Already Marked '{BNR_TC}' As Completed",
                        )

                else:
                    messagebox.showerror(
                        "Book Doesn't Exist",
                        f"'{BNR_TC}', Book Doesn't Exist In All Books.",
                    )

            else:
                messagebox.showerror(
                    "Field Empty",
                    "Please, Enter A Vaild Book Name To Mark As Completed",
                )

    # ----- Window Setttings -----
    Default_View_Window_Configuration("Mark As Completed")
    Opening_File_View_Content("Enter Book Name To Mark As Completed")

    Book_Name_MAR = TK.Entry(Window, font=Default_Font_Style)
    Book_Name_MAR.grid(row=4, column=0, sticky="")

    Button(
        Window,
        text="Completed",
        command=lambda Mark_Read="Mark_Read": Completed(Mark_Read),
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=5, column=0, sticky="")


# ------------------------------------------------------------------------------
# Remove a Book
def Remove_a_Book():

    def Remove_Book(RemoveBook):

        # ----- Opening File -----
        with open(User_Home_Books_File, "r") as Upadte_Read_Books_TXT:

            Reader_Obj = Upadte_Read_Books_TXT.read()  # str
            Dict_Reader_Obj = ast.literal_eval(Reader_Obj)  # str to dict using ast
            BNR_GET = Book_Name_Remove.get()
            BNR_GET = BNR_GET.strip()
            BNR_TC = BNR_GET.title()

            if not len(BNR_TC) == 0:
                if BNR_TC in Dict_Reader_Obj:
                    Dict_Reader_Obj.pop(BNR_TC)

                    # ----- Update .txt File -----
                    with open(User_Home_Books_File, "w") as Update_Books_TXT:
                        Update_Books_TXT.write(str(Dict_Reader_Obj))

                    Window.destroy()
                    messagebox.showinfo(
                        "Book Removed", f"You Removed '{BNR_TC}' From All Books."
                    )

                else:
                    messagebox.showerror(
                        "Book Doesn't Exist",
                        f"'{BNR_TC}', Book Doesn't Exist In All Books.",
                    )

            else:
                messagebox.showerror(
                    "Field Empty", "Please, Enter A Book Name To Remove."
                )

    # ----- Window Setttings -----
    Default_View_Window_Configuration("Remove Book")
    Opening_File_View_Content("Enter Book Name To Remove")

    Book_Name_Remove = TK.Entry(Window, font=Default_Font_Style)
    Book_Name_Remove.grid(row=4, column=0, sticky="")

    Button(
        Window,
        text="Remove",
        command=lambda RemoveBook="RemoveBook": Remove_Book(RemoveBook),
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=5, column=0, sticky="")


# ------------------------------------------------------------------------------
# Preferences
def Preferences():

    Window_Configuration("Preferences")  # F - Line 87

    def Save_Custom_Preferences():

        # ----- Clean_User_Aesthetics -----
        Custom_Aesthetics_User_List = []

        def Clean_User_Aesthetics(Custom_Aesthetic_Content):
            Custom_Aesthetic_Content = Custom_Aesthetic_Content.get()
            Custom_Aesthetic_Content = Custom_Aesthetic_Content.strip()
            Custom_Aesthetics_User_List.append(Custom_Aesthetic_Content)

        Custom_Aesthetics_Dict = Default_AFC.copy()

        Custom_Aesthetics_List = [
            Window_Size,
            Background_Color,
            Foreground_Color,
            Font_Style,
            Font_Size,
            Font_Design,
        ]

        for Custom_Aesthetic_Content in Custom_Aesthetics_List:
            Clean_User_Aesthetics(Custom_Aesthetic_Content)

        # ----- Update New User Settings In .txt File -----
        CAUL_Count = 0
        if not "" in Custom_Aesthetics_User_List:
            for Custom_Aesthetic_Content in Custom_Aesthetics_Dict:
                Custom_Aesthetics_Dict[Custom_Aesthetic_Content] = (
                    Custom_Aesthetics_User_List[CAUL_Count]
                )
                CAUL_Count += 1

            Window.destroy()
            Create_New_Aesthetics_File(Custom_Aesthetics_Dict)
            messagebox.showinfo(
                "Saved",
                "Applied Custom Preferences. Please, Restart Bookz To Read App.",
            )

        else:
            messagebox.showinfo(
                "Field Empty", "Field Is Found To Be Empty. Please, Fill It."
            )

    # ----- Restore_To_Default -----
    def Restore_To_Default():
        Create_New_Aesthetics_File(Default_AFC)
        Window.destroy()
        messagebox.showinfo(
            "Saved", "Applied Deafult Preferences. Please, Restart Bookz To Read App."
        )

    # -----	About_Label_HV -----
    def About_Label_HV(About_Labels, Column_Num):
        AL_Count = 16
        for About_Label in About_Labels:
            Label(
                Window,
                text=About_Label,
                font=Default_Font_Style,
                bg=Default_B_G,
                fg=Default_F_G,
            ).grid(row=AL_Count, column=Column_Num)
            AL_Count += 1

    # ----- Headings -----
    Preferences_Labels = ["Preference Style", "Custom Preference", "Default Preference"]
    P_Count = 0
    for Preference_Labels in Preferences_Labels:
        Label(
            Window,
            text=Preference_Labels,
            font=Default_Font_Style,
            bg=Default_B_G,
            fg=Default_F_G,
        ).grid(row=0, column=P_Count)
        P_Count += 1

    # ----- On Screen Labels -----
    Aesthetics_Labels = [
        "",
        "Window Size",
        "Background Color",
        "Foreground Color",
        "Font Style",
        "Font Size",
        "Font Design",
    ]
    A_Count = 1
    for Aesthetics_Label in Aesthetics_Labels:
        Label(
            Window,
            text=Aesthetics_Label,
            font=Default_Font_Style,
            bg=Default_B_G,
            fg=Default_F_G,
        ).grid(row=A_Count, column=0)
        A_Count += 1

    # ----- Get Values -----
    Window_Size = TK.Entry(Window, font=Default_Font_Style)
    Window_Size.grid(row=2, column=1)

    Background_Color = TK.Entry(Window, font=Default_Font_Style)
    Background_Color.grid(row=3, column=1)

    Foreground_Color = TK.Entry(Window, font=Default_Font_Style)
    Foreground_Color.grid(row=4, column=1)

    Font_Style = TK.Entry(Window, font=Default_Font_Style)
    Font_Style.grid(row=5, column=1)

    Font_Size = TK.Entry(Window, font=Default_Font_Style)
    Font_Size.grid(row=6, column=1)

    Font_Design = TK.Entry(Window, font=Default_Font_Style)
    Font_Design.grid(row=7, column=1)

    Button(
        Window,
        text="Save Custom",
        command=Save_Custom_Preferences,
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=8, column=1)

    # ----- Default Style -----
    AFC_Count = 2
    for AFC_Contents in Default_AFC.values():
        Label(
            Window,
            text=AFC_Contents,
            font=Default_Font_Style,
            bg=Default_B_G,
            fg=Default_F_G,
        ).grid(row=AFC_Count, column=2)
        AFC_Count += 1

    Button(
        Window,
        text="Restore To Default",
        command=Restore_To_Default,
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=8, column=2)

    # ----- About -----
    for Empty_Label in range(9, 14):
        Label(
            Window, text="", font=Default_Font_Style, bg=Default_B_G, fg=Default_F_G
        ).grid(row=Empty_Label, column=1)
        Empty_Label += 1

    Label(
        Window,
        text="...About...",
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).grid(row=15, column=0)

    About_Labels_C0 = [
        "Application Name",
        "Designed and Developed by",
        "GitHub",
        "Created On",
        "Last Updated",
    ]

    About_Label_HV(About_Labels_C0, 0)

    About_Labels_C1 = [
        "Bookz To Read",
        "Raghava, KV CBE. ",
        "@raghavtwenty",
        "19 July 2021",
        "10 May 2024",
    ]
    About_Label_HV(About_Labels_C1, 1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Home Window On Screen Contents

# ----- Home Window Labels -----
Label(
    Window,
    text="Bookz To Read",
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(pady=10)

HW_Label = ["Home Menu", "Hello ..."]

for Content_HW_Label in HW_Label:
    Label(
        Window,
        text=Content_HW_Label,
        font=Default_Font_Style,
        bg=Default_B_G,
        fg=Default_F_G,
    ).pack(fill=TK.X, padx=250, pady=20)

# ----- Home Window Buttons -----
Button(
    Window,
    text="View Books",  # F-222
    command=View_Books,
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(fill=TK.X, padx=250, pady=5)

Button(
    Window,
    text="Find Similarities",  # F-240
    command=Sort_Duplicates,
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(fill=TK.X, padx=250, pady=5)

Button(
    Window,
    text="Add a Book",  # F-319
    command=Add_a_Book,
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(fill=TK.X, padx=250, pady=5)

Button(
    Window,
    text="Mark as Completed",  # F-390
    command=Mark_As_Read,
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(fill=TK.X, padx=250, pady=5)

Button(
    Window,
    text="Remove a Book",  # F-447
    command=Remove_a_Book,
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(fill=TK.X, padx=250, pady=5)

Button(
    Window,
    text="Preferences",  # F-496
    command=Preferences,
    font=Default_Font_Style,
    bg=Default_B_G,
    fg=Default_F_G,
).pack(fill=TK.X, padx=250, pady=5)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Mainloop

Window.mainloop()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
