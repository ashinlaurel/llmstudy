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
  dtype_spec = {
      'review_id': 'int64',
      'rating': 'int64',
      'title': 'string',
      'text': 'string'
  }

  examples_file_path = os.path.join('./', '50 Examples.xlsx')
  examples_df = pd.read_excel(examples_file_path, dtype=dtype_spec)
  examples_df = examples_df.filter(['helpfulness', 'rating', 'title', 'text'])
  examples_json_string = examples_df.to_json(orient='records', indent=4)

  prompt = f"""As a data scientist analyzing the usefulness of reviews on e-commerce platforms, your goal is to determine how helpful each review is in assisting a customer in deciding whether to purchase a product. Included below are details about a product called META and a set of reviews with human-provided scores indicating their usefulness.   Use the following refined criteria and scoring rubric, drawing from literature on review helpfulness and user perception.

META:

Product Name	: Amazon Brand Mama Bear Gentle Touch Diapers, Hypoallergenic, Size 5, 33 Count, White

Product Description: 33 size 5 diapers for babies 27+ lbs (12+ kg)', 'First-time users, consider getting the size your cub currently wears. If the fit is snug, size up (which provides extra absorbency)', 'Hypoallergenic and dermatologist tested', 'Free from chlorine bleaching, perfumes, lotions, parabens, and phthalates', 'Diapers at a great value with up to 12 hours of leakage protection; Wetness indicator shows when it’s time for a change', 'Thin design with flexible fit for comfortable movement', 'Breathable outer cover helps keep baby’s skin dry and healthy', 'Produced in a zero waste to landfill facility; Cruelty free - not tested on animals', 'Satisfaction Guarantee: We’re proud of our products. If you aren’t satisfied, we’ll refund you for any reason within a year of purchase.', 'An Amazon brand'

About the Product : Mama Bear Gentle Touch Diapers. Gentle on skin. Cute on behinds. Our diapers offer trusted leakage protection, secure fit, and cozy comfort. They’re hypoallergenic and made with a soft, breathable outer cover to help keep your baby comfortable day and night. Our diapers are rigorously tested for quality and effectiveness, and your satisfaction is guaranteed.


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

Reference Reviews:
The following are a set of reviews which are human labelled.
Each object contains the following fields:

1. "rating": The star rating given by the customer.
2. "title": The title of the review.
3. "text": The actual review text.
4. “helpfulness” : This is the human assigned score for the review based on how helpful the review is.

The reference reviews are : {examples_json_string}


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
{{
  "Reviews": [
    {{
      "helpfulness": 4,
      "review_id": "12345",
    }},
    {{
      "helpfulness": 2,
      "review_id": "67890",
    }}
  ]
}}
```

### Notes:
- Score each review individually, regardless of similarity to other reviews.
- It is crucial that all reviews are processed and included in the output.
- Consider using language processing techniques to ensure the readability and emotional intelligence criteria are accurately evaluated.
"""

  current_model="gemini-1.5-pro"
  product_id = 'Baby_products'
  directory_path = os.path.join('./', current_model, 'finetune')


  os.makedirs(directory_path ,exist_ok=True)

  file_path = './' + '/base.xlsx'

  df = pd.read_excel(file_path, sheet_name='Reviews', dtype=dtype_spec)
  df = df.drop(columns=['helpfulness'])

  combined_df = pd.DataFrame()

  genai.configure(api_key='API KEY')

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

  combined_df.to_csv("./{}".format(current_model)+ "/finetune"+ "/{}.csv".format(datetime.now()), index=False)


  all_present=df['review_id'].isin(combined_df['review_id']).all()
  print(f"Are all review_id values in df present in combined_df? {all_present}")

  df1_not_in_df2 = df[~df['review_id'].isin(combined_df['review_id'])]
  print("Rows in df but not in combined df based on 'review_id': ", df1_not_in_df2)

  df2_not_in_df1 = combined_df[~combined_df['review_id'].isin(df['review_id'])]
  print("Rows in combined but not in df based on 'review_id': ", df2_not_in_df1)

  print(f"Number of unique review_id values: {combined_df['review_id'].nunique()}")

  print(f"Number of missing values in 'helpfulness' column: {combined_df['helpfulness'].isnull().sum()}")


main()