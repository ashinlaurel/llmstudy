import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os


def main():

    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/non_meta_output.txt'
    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4-turbo_non_meta_output.txt'
    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4-turbo_finetune_output.txt'
    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/finetune_with_own_output.txt'


    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125_non_meta_output.txt'
    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125_meta_output.txt'
    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125_finetune_with_own_output.txt'


    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/meta_output.txt'
    # output_file_path = 'Dataset/Baby_Products_B0BMQ3G124/finetune_output.txt'

    # output_file_path = 'Dataset/Appliances_B0BX9GK3PB/non_meta_output.txt'
    # output_file_path = 'Dataset/Appliances_B0BX9GK3PB/meta_output.txt'
    # output_file_path = 'Dataset/Appliances_B0BX9GK3PB/finetune_output.txt'
    output_file_path = 'Dataset/Appliances_B0BX9GK3PB/finetune_with_own_output.txt'



    with open(output_file_path, 'w') as file:
        # This block will clear the file
        pass

    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4o/non_meta/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4-turbo/non_meta/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4-turbo/finetune/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4o/finetune_with_own/'


    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125/non_meta/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125/meta/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125/finetune/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-3.5-turbo-0125/finetune_with_own/'



    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4o/meta/'
    # input_folder_path1 = 'Dataset/Baby_Products_B0BMQ3G124/gpt-4o/finetune/'

    # input_folder_path1 = 'Dataset/Appliances_B0BX9GK3PB/gpt-4o/non_meta/'
    # input_folder_path1 = 'Dataset/Appliances_B0BX9GK3PB/gpt-4o/meta/'
    # input_folder_path1 = 'Dataset/Appliances_B0BX9GK3PB/gpt-4o/finetune/'
    input_folder_path1 = 'Dataset/Appliances_B0BX9GK3PB/gpt-4o/finetune_with_own/'




    # input_file_path2 = 'Dataset/Baby_Products_B0BMQ3G124/human_mean.xlsx'
    input_file_path2 = 'Dataset/Appliances_B0BX9GK3PB/human_mean.xlsx'

    # Get a list of files in the directory with their creation times
    files_with_ctime = [(filename, os.path.getctime(os.path.join(input_folder_path1, filename)))
                        for filename in os.listdir(input_folder_path1)
                        if os.path.isfile(os.path.join(input_folder_path1, filename))]

    # Sort the files by creation time in descending order (latest first)
    sorted_files = sorted(files_with_ctime, key=lambda x: x[1], reverse=True)

    # Extract just the filenames in sorted order
    # sorted_filenames = [filename for filename, ctime in sorted_files]

    for filename, _ in sorted_files:
        input_file_path1 = os.path.join(input_folder_path1, filename)
        df1 = pd.read_csv(input_file_path1)
        print(f"Number of missing values in 'helpfulness' column: {df1['helpfulness'].isnull().sum()}")

        df2 = pd.read_excel(input_file_path2)

        with open(output_file_path, 'a') as file:
            file.write(input_file_path1 + '\n')
            file.write(input_file_path2 + '\n')

        # Ensure the 'helpfulness' columns are numeric
        df1['helpfulness'] = pd.to_numeric(df1['helpfulness'], errors='coerce')
        df2['helpfulness'] = pd.to_numeric(df2['helpfulness'], errors='coerce')

        # Merge the DataFrames on the 'review_id' column
        merged_df = pd.merge(df1, df2, on='review_id', suffixes=('_file1', '_file2'))

        # Drop rows with NaN values in 'helpfulness' columns after the merge
        merged_df.dropna(subset=['helpfulness_file1', 'helpfulness_file2'], inplace=True)

        # Calculate the RMSE between the 'helpfulness' columns
        rmse = np.sqrt(mean_squared_error(merged_df['helpfulness_file1'], merged_df['helpfulness_file2']))

        # Calculate the MAE between the 'helpfulness' columns
        mae = mean_absolute_error(merged_df['helpfulness_file1'], merged_df['helpfulness_file2'])

        helpfulness_human_mean = df2['helpfulness'].mean()
        helpfulness_human_std = df2['helpfulness'].std()

        helpfulness_llm_mean = df1['helpfulness'].mean()
        helpfulness_llm_std = df1['helpfulness'].std()



        # Print the RMSE
        with open(output_file_path, 'a') as file:
            print(f"Root Mean Square Error (RMSE): {rmse}")
            file.write(f"Root Mean Square Error (RMSE): {rmse}\n")

            print(f"Mean Absolute Error (MAE): {mae}")
            file.write(f"Mean Absolute Error (MAE): {mae}\n")

            print(f"Human mean:  {helpfulness_human_mean}")
            file.write(f"Human mean:  {helpfulness_human_mean}\n")

            print(f"Human st. dev:  {helpfulness_human_std}")
            file.write(f"Human st. dev:  {helpfulness_human_std}\n")

            print(f"LLM mean:  {helpfulness_llm_mean}")
            file.write(f"LLM mean:  {helpfulness_llm_mean}\n")

            print(f"LLM st. dev:  {helpfulness_llm_std}")
            file.write(f"LLM st. dev:  {helpfulness_llm_std}\n")





if __name__ == "__main__":
    main()