import pandas as pd

def cleaner(input_path, output_path):

    df_unclean = pd.read_parquet(input_path)
    print('------------------------------------------------------------------')
    print('Data before cleaning:')
    df_unclean.info()
    print(
        f"Count of rows with a missing or negative length_of_stay value: "
        f"{((df_unclean['length_of_stay'] < 0) | (df_unclean['length_of_stay'].isna())).sum()}"
    )

    #  The assumption is that cats with a negative number of days of stay are due to data entry errors for availableDate or adoptedDate

    print('------------------------------------------------------------------')
    df_clean = df_unclean[(df_unclean['length_of_stay'].notna()) & (df_unclean['length_of_stay'] >= 0)]
    print('Cleaned data:')
    df_clean.info()


    sorted_df = df_clean['length_of_stay'].sort_values()
    print('Checking for negative values:')
    print(sorted_df.min()) #  check for negative days

  
    df_clean.to_parquet(output_path)
    print('Data is ready for EDA')
    print(f'Clean parquet file saved to {output_path}')