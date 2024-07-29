import time

from openai import OpenAI
import json
import csv
import pandas as pd
from datetime import datetime
import os


def dataframe_chunker(df, batch_size):
    for pos in range(0, len(df), batch_size):
        yield df.iloc[pos:pos + batch_size]


def main():

    client = OpenAI(
        api_key='API_KEY',
    )

    prompt = """As a data scientist analyzing the usefulness of reviews on e-commerce platforms, your goal is to determine how helpful each review is in assisting a customer in deciding whether to purchase a product. Use the following scoring rubric, drawing from literature on review helpfulness and user perception.

### Rubric Scoring:

When rating reviews, apply the following criteria systematically. Each criterion is rated on a scale from 1 to 5, where:

- **1**: Very poor
- **2**: Poor
- **3**: Average
- **4**: Good
- **5**: Excellent

1. Specificity and Detail
2. Length and Conciseness
3. Balanced Perspective
4. Constructive Sentiment
5. Readability
6. Comparative Insights
7. Emotionally Intelligent Language
8. Relevance to the Product
9. Use of Evidence
10. User Experience Context
11. Consistency with Rating

Final Scoring:

Calculate the average score across all criteria provided above and assign a helpfulness score from 1-5.

### Input:
You will receive a JSON array with multiple objects representing user reviews of a product from Amazon. Each object contains the following fields:
1. "review_id": A unique identifier for the review.
2. "rating": The star rating given by the user.
3. "title": The title of the review.
4. "text": The actual review text.

### Output:
Return a JSON array under the key "Reviews". Each object in the array should contain the following fields:
1. "helpfulness": Helpfulness score (1-5). Type should be int64.
2. "review_id": The review_id of the review. Type should be int64.

### Example Output:
```json
{
  "Reviews": [
    {
      "helpfulness": 4,
      "review_id": "12345"
    },
    {
      "helpfulness": 2,
      "review_id": "67890"
    }
  ]
}
```

### Notes:
- Score each review individually, regardless of similarity to other reviews.
- It is crucial that all reviews are processed and included in the output.
- Consider using language processing techniques to ensure the readability and emotional intelligence criteria are accurately evaluated.
\n"""

    # model = "gpt-3.5-turbo-0125"
    # model = "gpt-4-turbo"
    model = "gpt-4o"

    product_id = 'Baby_Products_B0BMQ3G124'

    # Define the directory path
    directory_path = os.path.join('./Dataset', product_id, model, 'non_meta')

    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    file_path = './Dataset/' + product_id + '/base.xlsx'
    dtype_spec = {
        'review_id': 'int64',  # Read as integer
        'rating': 'int64',  # Read as integer
        'title': 'string',  # Read as string
        'text': 'string'  # Read as string
    }
    df = pd.read_excel(file_path, sheet_name='Reviews', dtype=dtype_spec)
    df = df.drop(columns=['helpfulness'])
    # print(df)

    combined_df = pd.DataFrame()

    # Fetch 20 rows at a time
    batch_count = 0
    for chunk in dataframe_chunker(df, batch_size=10):
        print(f'Batch {batch_count} processing')

        # print(len(chunk), " rows fetched")
        chunk_json = chunk.to_json(orient='records', indent=4)
        review_sugar = "Reviews: \n" + str(chunk_json) + "\n"
        # print(review_sugar)

        content = prompt + review_sugar
        # print(content)

        chat_completion_json_object = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": str(content)
                }
            ],
            model=model,
            response_format={
                "type": "json_object",
            },
        )

        # Parse the JSON string into a Python dictionary
        # response_json = json.loads(chat_completion_json_object.choices[0].message.content)
        # print(chat_completion_json_object.choices[0].message.content)
        print(f'Batch {batch_count} succeeded')

        # Parse the JSON string into a Python dictionary
        response_json = json.loads(chat_completion_json_object.choices[0].message.content)
        # Extract the list of reviews
        reviews_list = response_json['Reviews']

        chunk_df = pd.DataFrame(reviews_list)
        # print(len(chunk_df))
        # print("Response: \n", chunk_df)

        combined_df = pd.concat([combined_df, chunk_df], ignore_index=True)
        # print(len(combined_df))
        time.sleep(2)
        batch_count+=1

    all_present = df['review_id'].isin(combined_df['review_id']).all()
    # Print the result
    print(f"Are all review_id values in df present in combined_df? {all_present}")

    df1_not_in_df2 = df[~df['review_id'].isin(combined_df['review_id'])]
    print("Rows in df but not in combined_df based on 'review_id':", df1_not_in_df2)

    df2_not_in_df1 = combined_df[~combined_df['review_id'].isin(df['review_id'])]
    print("Rows in combined_df but not in df based on 'review_id':", df2_not_in_df1)

    print(f"Number of unique review_id values: {combined_df['review_id'].nunique()}")

    # Count the number of missing values in the 'helpfulness' column
    print(f"Number of missing values in 'helpfulness' column: {combined_df['helpfulness'].isnull().sum()}")

    combined_df.to_csv('./Dataset' + "/{}".format(product_id) + "/{}".format(model)+ "/non_meta"+ "/{}.csv".format(datetime.now()),
                       index=False)


if __name__ == "__main__":
    main()
