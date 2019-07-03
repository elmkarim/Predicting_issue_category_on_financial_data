#Function to load data into dataframe
def load_excel_spreadsheet (filename,spreadsheet):
    # Load spreadsheet
    import pandas
    xl = pandas.ExcelFile(filename)

    # Print the sheet names
    print('Sheets in file: ', xl.sheet_names)

    # Load a sheet into a DataFrame by name: df1
    df = xl.parse(spreadsheet)
    print('Data loaded from sheet:', spreadsheet)
    
    return(df)


#Load serialized objects from pickle file
def load_from_pickle(filename):
    import pickle
    with open(filename, "rb") as f:
        return (pickle.load(f))

#Save serialized objects from pickle file
def save_to_pickle(filename, objects):
    import pickle
    with open(filename, "wb") as f:
        pickle.dump(objects, f)
        