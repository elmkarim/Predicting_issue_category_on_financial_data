import helper_save_load

df = helper_save_load.load_excel_spreadsheet("data/Commentaries_labeled_v3.xlsx", "MergedLabels")
brands_df = helper_save_load.load_excel_spreadsheet("data/brands-categories-totals-updated.xlsx", "Brands-processed")
brands_df.rename(columns={"Brands in Commentaries file":"Brand"}, inplace=True)

df = df.merge(brands_df[["Brand", "Brand_1", "Brand_2", "Brand_3"]], on=["Brand"])
df.sort_values(by=["Num"], inplace=True)

helper_save_load.save_to_pickle("Labeled_comments2.pkl", df)
