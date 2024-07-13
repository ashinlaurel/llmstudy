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

def dataframe_chunker(df, batch_size):
  for pos in range(0, len(df), batch_size):
    yield df.iloc[pos:pos+batch_size]

# class Reviews(typing.TypedDict):
#   review_id: int64
#   helpfulness: int64

class Review(typing.TypedDict):
    helpfulness: int
    review_id: int

class ReviewsResponse(typing.TypedDict):
    Reviews: list[Review]

def main():
  prompt = """As a data scientist analyzing the usefulness of reviews on e-commerce platforms, your goal is to determine how helpful each review is in assisting a customer in deciding whether to purchase a product. Use the following refined criteria and scoring rubric, drawing from literature on review helpfulness and user perception.

Criteria for rating reviews :
When rating reviews, apply the following criteria systematically:
- Examine the review's content for specificity and detail.
- Consider the review's length and ensure it strikes a balance between being thorough and concise.
- Check the credibility of the reviewer, focusing on verified purchases and expertise.
- Look for a balanced perspective that includes both pros and cons.
- Evaluate the sentiment for constructiveness and neutrality.*
- Ensure the review is readable and well-written.
- Value comparative insights provided by the reviewer.


### Rubric Scoring:

When rating reviews, apply the following criteria systematically. Each criterion is rated on a scale from 1 to 5, where:

- **1**: Very poor
- **2**: Poor
- **3**: Average
- **4**: Good
- **5**: Excellent

1. Specificity and Detail:
2. Length and Conciseness:
3. Balanced Perspective:
4. Constructive Sentiment:
5. Readability:
6. Comparative Insights:
7. Emotionally Intelligent Language:
8. Relevance to the Product:
9. Use of Evidence:
10. User Experience Context:
11. Consistency with Rating:

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
      "review_id": "12345",
    },
    {
      "helpfulness": 2,
      "review_id": "67890",
    }
  ]
}
```

### Notes:
- Score each review individually, regardless of similarity to other reviews.
- It is crucial that all reviews are processed and included in the output.
- Consider using language processing techniques to ensure the readability and emotional intelligence criteria are accurately evaluated.
"""

  current_model="gemini-1.5-pro"
  product_id = 'Baby_products'

  directory_path = os.path.join('./', current_model, 'zero_shot')


  os.makedirs(directory_path ,exist_ok=True)

  file_path = './' + '/base.xlsx'

  dtype_spec = {
      'review_id': 'int64',
      'rating': 'int64',
      'title': 'string',
      'text': 'string'
  }
  df = pd.read_excel(file_path, sheet_name='Reviews', dtype=dtype_spec)
  df = df.drop(columns=['helpfulness'])

  combined_df = pd.DataFrame()

  genai.configure(api_key='AIzaSyAboVn4nABtXIBDljroWSV4yf2XNFZdQhA')

  model = genai.GenerativeModel(model_name='models/'+current_model)
  gen_config = genai.GenerationConfig(response_mime_type="application/json",
                                            response_schema = ReviewsResponse)

  batch_count = 0

  for chunk in dataframe_chunker(df, batch_size=10):
    print(f'Batch {batch_count} processing')

    chunk_json = chunk.to_json(orient='records', indent=4)
    review_sugar = "Reviews: \n" + str(chunk_json) + "\n"

    content = prompt + review_sugar


    result = model.generate_content(
    content,
    generation_config=gen_config)

    print(result.text)
    print(f'Batch {batch_count} succeeded')

    response_json = json.loads(result.text)
    reviews_list = response_json['Reviews']

    chunk_df = pd.DataFrame(reviews_list)

    combined_df = pd.concat([combined_df, chunk_df], ignore_index=True)

    time.sleep(2)
    batch_count+=1

  all_present=df['review_id'].isin(combined_df['review_id']).all()
  print(f"Are all review_id values in df present in combined_df? {all_present}")

  df1_not_in_df2 = df[~df['review_id'].isin(combined_df['review_id'])]
  print("Rows in df but not in combined df based on 'review_id': ", df1_not_in_df2)

  df2_not_in_df1 = combined_df[~combined_df['review_id'].isin(df['review_id'])]
  print("Rows in df but not in combined df based on 'review_id': ", df2_not_in_df1)

  print(f"Number of unique review_id values: {combined_df['review_id'].nunique()}")

  print(f"Number of missing values in 'helpfulness' column: {combined_df['helpfulness'].isnull().sum()}")

  combined_df.to_csv("./{}".format(current_model)+ "/zero_shot"+ "/{}.csv".format(datetime.now()), index=False)


main()