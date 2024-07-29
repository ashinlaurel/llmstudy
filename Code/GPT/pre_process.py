import os
import pandas as pd

# product_id = 'Baby_Products_B0BMQ3G124'
product_id = 'Appliances_B0BX9GK3PB'

# Define the path to the folder containing the Excel files
folder_path = './Dataset/' + product_id + '/human_labelled/'

# Initialize an empty DataFrame to store the combined data
all_data = pd.DataFrame()

custom_header = ['review_id', 'helpfulness', 'rating', 'title', 'text']

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    print(filename)
    if filename.endswith('.xlsx'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        # Read the "Reviews" sheet into a DataFrame
        df = pd.read_excel(file_path, sheet_name='Reviews', header=None, skiprows=1)
        df.columns = custom_header

        # Append the data to the combined DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)

print(all_data)
# Calculate the mean score for each review_id
mean_scores = all_data.groupby('review_id')['helpfulness'].mean().reset_index()

# Print the results
print(mean_scores)

# Optionally, save the results to a new Excel file
mean_scores.to_excel('./Dataset/' + product_id + '/human_mean' + '.xlsx', index=False)