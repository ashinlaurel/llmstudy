import google.generativeai as genai
from google.colab import userdata
import google.generativeai as genai
import typing_extensions as typing
import json
import dataclasses
import typing_extensions as typing
import pandas as pd
import os
from datetime import datetime
import time
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

def main():
    output_file_path = './zero_shot_output.txt'

    with open(output_file_path, 'w') as file:
      pass

    input_folder_path1 = './gemini-1.5-pro/zero_shot/'


    input_file_path2 = './human_mean.xlsx'

    files_with_ctime = [(filename, os.path.getctime(os.path.join(input_folder_path1, filename)))
                        for filename in os.listdir(input_folder_path1)
                        if os.path.isfile(os.path.join(input_folder_path1, filename))]

    sorted_files = sorted(files_with_ctime, key=lambda x:x[1], reverse=True)

    for filename, _ in sorted_files:
      input_file_path1 = os.path.join(input_folder_path1, filename)
      df1 = pd.read_csv(input_file_path1)
      print(f"Number of missing values in 'helpfulness' column: {df1['helpfulness'].isnull().sum()}")

      df2 = pd.read_excel(input_file_path2)

      with open(output_file_path, 'a') as file:
        file.write(input_file_path1 + '\n')
        file.write(input_file_path2 + '\n')


      df1['helpfulness'] = pd.to_numeric(df1['helpfulness'], errors='coerce')
      df2['helpfulness'] = pd.to_numeric(df2['helpfulness'], errors='coerce')

      merged_df = pd.merge(df1, df2, on='review_id', suffixes=('_file1', '_file2'))

      merged_df.dropna(subset=['helpfulness_file1', 'helpfulness_file2'], inplace=True)

      rmse = np.sqrt(mean_squared_error(merged_df['helpfulness_file1'], merged_df['helpfulness_file2']))

      mae = mean_absolute_error(merged_df['helpfulness_file1'], merged_df['helpfulness_file2'])

      helpfulness_human_mean = df2['helpfulness'].mean()
      helpfulness_human_std = df2['helpfulness'].std()

      helpfulness_llm_mean = df1['helpfulness'].mean()
      helpfulness_llm_std = df1['helpfulness'].std()

      with open(output_file_path, 'a') as file:
        file.write(f"RMSE: {rmse}\n")
        file.write(f"MAE: {mae}\n")
        file.write(f"Human mean: {helpfulness_human_mean}\n")
        file.write(f"Human st.dev: {helpfulness_human_std}\n")
        file.write(f"LLM mean: {helpfulness_llm_mean}\n")
        file.write(f"LLM st.dev: {helpfulness_llm_std}\n")

main()
