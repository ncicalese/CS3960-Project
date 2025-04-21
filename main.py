# This code creates a simple interface for PD-Explain to make the library more accessible to whomever would like to
# explore a dataset
# Code Written by Nicholas Cicalese

# Some places I got help with tkinter:
# https://www.youtube.com/watch?v=epDKamC-V-8
# https://stackoverflow.com/questions/18675266/how-to-make-matplotlibpyplot-resizeable-with-the-tkinter-window-in-python
# https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
# https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
# https://stackoverflow.com/questions/66946210/run-function-when-an-item-is-selected-from-a-dropdown

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
import pd_explain


# This method opens a csv file
def open_file():
    global df
    global selectedColumn

    filepath = filedialog.askopenfilename()
    openFileLabel.config(text=filepath)

    df = pd.read_csv(filepath)

    int_cols = list(df.select_dtypes(include='int').columns)

    selectedColumn = StringVar(window)
    selectedColumn.set(int_cols[0])
    selectedColumn.trace('w', column_changed)

    noColumnsFound.destroy()
    options = OptionMenu(window, selectedColumn, *int_cols)
    options.config(font="Helvetica 16")
    options.grid(row=1, column=1)

# This method calls PD-Explain's explain method to visualize an explanation of the data
def explain_clicked():
    filter = selectedFilter.get()
    column = selectedColumn.get()
    threshold = int(thresholdValueEntry.get())

    if filter == "<":
        filtered_df = df[df[column] < threshold]
    elif filter == "<=":
        filtered_df = df[df[column] <= threshold]
    elif filter == ">":
        filtered_df = df[df[column] > threshold]
    elif filter == ">=":
        filtered_df = df[df[column] >= threshold]
    elif filter == "==":
        filtered_df = df[df[column] == threshold]
    else:
        filtered_df = df[df[column] != threshold]

    filtered_df.explain(top_k=int(explanationNumberEntry.get()), figs_in_row=2)
    plt.show()

# This method updates the column range when a new column is selected
def column_changed(*args):
    global df

    min = df[selectedColumn.get()].min()
    max = df[selectedColumn.get()].max()

    columnRange.config(text=str(min) + " to " + str(max))


df = None
selectedColumn = None

window = Tk()
window.geometry("600x400")

# Open File
openFileButton = Button(window, text="Open File", font='Helvetica 16 bold', command=open_file)
openFileButton.grid(row=0, column=0, pady=10)
openFileLabel = Label(window, text="No File Selected", font='Helvetica 16')
openFileLabel.grid(row=0, column=1)

# Column Name
columnNameLabel = Label(window, text="Column Name:", font='Helvetica 16 bold')
columnNameLabel.grid(row=1, column=0, pady=10)
noColumnsFound = Label(window, text="No Columns Found", font='Helvetica 16')
noColumnsFound.grid(row=1, column=1)

# Column Range
columnRangeLabel = Label(window, text="Column Range:", font="Helvetica 16 bold")
columnRangeLabel.grid(row=2, column=0, pady=10)
columnRange = Label(window, text="No Column Selected", font="Helvetica 16")
columnRange.grid(row=2, column=1)

# Filter Type
filterTypeLabel = Label(window, text="Filter Type:", font="Helvetica 16 bold")
filterTypeLabel.grid(row=3, column=0, pady=10)
filterTypeList = ["<", "<=", ">", ">=", "==", "!="]
selectedFilter = StringVar(window)
selectedFilter.set(filterTypeList[0])
filterDropdown = OptionMenu(window, selectedFilter, *filterTypeList)
filterDropdown.config(font="Helvetica 16")
filterDropdown.grid(row=3, column=1)

# Threshold Value
thresholdValueLabel = Label(window, text="Threshold Value:", font="Helvetica 16 bold")
thresholdValueLabel.grid(row=4, column=0, pady=10)
thresholdValueEntry = Entry(window, width=10)
thresholdValueEntry.config(font="Helvetica 16")
thresholdValueEntry.grid(row=4, column=1)

# Number of Explanations
explanationLabel = Label(window, text="Number of Explanations:", font='Helvetica 16 bold')
explanationLabel.grid(row=5, column=0, pady=10)
explanationNumberEntry = Entry(window, width=10)
explanationNumberEntry.config(font="Helvetica 16")
explanationNumberEntry.grid(row=5, column=1)
explanationNumberEntry.insert(index=0, string="1")

# Explain Button
explainButton = Button(window, text="Explain!", font="Helvetica 16 bold", command= lambda: explain_clicked())
explainButton.grid(row=6, pady=10)

window.mainloop()
