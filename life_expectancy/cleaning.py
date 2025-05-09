"""
This module cleans the raw life expectancy dataset and converts it into a dataset 
for Portugal by default. You can also specify a different country for the dataset.
"""

import os
import argparse
import pandas as pd

def clean_data(country_code='PT'):
    """
    Cleans and processes the raw life expectancy data by:
    - Splitting 'unit,sex,age,geo\\time' into separate columns
    - Filtering for Portuguese data (by default)
    - Melting the DataFrame to reshape it
    - Cleaning up the 'value' column and converting it to numeric
    - Saving the cleaned DataFrame as a CSV file
    """

    # Path to the raw data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    file_path = os.path.join(project_dir, 'life_expectancy', 'data', 'eu_life_expectancy_raw.tsv')
    # Reading the raw data file
    life_expectancy_df = pd.read_csv(file_path, sep='\t')

    # removing spaces in variable names
    life_expectancy_df.columns = life_expectancy_df.columns.str.replace(' ', '')

    # creating new variables by separating "unit,sex,age,geo\time"
    life_expectancy_df[['unit', 'sex', 'age', 'region']] = (
        life_expectancy_df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    )
    # Dropping 'unit,sex,age,geo\\time' column
    life_expectancy_df = life_expectancy_df.drop('unit,sex,age,geo\\time', axis=1)

    # filtering by portuguese data
    life_expectancy_df = life_expectancy_df[life_expectancy_df['region'] == country_code]

    # Melt the dataframe and clean up missing values (":")
    life_expectancy_df_melted = pd.melt(
        life_expectancy_df,
        id_vars=['unit', 'sex', 'age', 'region'],
        var_name='year',
        value_name='value'
    ).query('value != ": "')

    # Clean 'value' and altering data type to float
    life_expectancy_df_melted['value'] = pd.to_numeric(
        life_expectancy_df_melted['value'].str.replace(r'[^0-9.^0-9]', '', regex=True),
        errors='coerce'
        )
    # Altering 'year' data type to integer
    life_expectancy_df_melted['year'] = life_expectancy_df_melted['year'].astype(int)

    # Save the cleaned DataFrame to a .csv file called "pt_life_expectancy.csv"
    output_file_path = os.path.join(
        project_dir,
        'life_expectancy',
        'data',
        f'{country_code}_life_expectancy.csv'
        )
    life_expectancy_df_melted.to_csv(output_file_path, index=False)

    return life_expectancy_df_melted

# If the script is executed directly, this block will be run to clean data
if __name__ == '__main__':  # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument('--country', default='PT')
    args = parser.parse_args()

    clean_data(country_code=args.country)
