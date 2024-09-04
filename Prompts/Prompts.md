# Prompts
## Zero-Shot

As a data scientist analyzing the usefulness of reviews on e-commerce platforms, your goal is to determine how helpful each review is in assisting a customer in deciding whether to purchase a product. Use the following refined criteria and scoring rubric, drawing from literature on review helpfulness and user perception.
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
3. "reason": A brief reason explaining the score.

### Example Output:
```json
{
  "Reviews": [
    {
      "helpfulness": 4,
      "review_id": "12345",
      "reason": "The review is detailed and balanced but lacks specific comparative insights."
    },
    {
      "helpfulness": 2,
      "review_id": "67890",
      "reason": "The review is too short and biased, providing little useful information."
    }
  ]
}
```

### Notes:
- Score each review individually, regardless of similarity to other reviews.
- It is crucial that all reviews are processed and included in the output.
- Consider using language processing techniques to ensure the readability and emotional intelligence criteria are accurately evaluated.

Please now rate the following reviews:
`<Review List>

## Few Shot 1

As a data scientist analyzing the usefulness of reviews on e-commerce platforms, your goal is to determine how helpful each review is in assisting a customer in deciding whether to purchase a product. You also contain the details about the product known as META which is provided below.  Use the following refined criteria and scoring rubric, drawing from literature on review helpfulness and user perception.

META:

Product Name	: `<Product Name>`
Product Description: `<Product Description>`
About the Product :  `<About the Product>`


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
3. "reason": A brief reason explaining the score.
### Example Output:
```json
{
  "Reviews": [
    {
      "helpfulness": 4,
      "review_id": "12345",
      "reason": "The review is detailed and balanced but lacks specific comparative insights."
    },
    {
      "helpfulness": 2,
      "review_id": "67890",
      "reason": "The review is too short and biased, providing little useful information."
    }
  ]
}
```
### Notes:
- Score each review individually, regardless of similarity to other reviews.
- It is crucial that all reviews are processed and included in the output.
- Consider using language processing techniques to ensure the readability and emotional intelligence criteria are accurately evaluated.

Please now rate the following reviews:
`<Review List>`
## Few Shot 2

As a data scientist analyzing the usefulness of reviews on e-commerce platforms, your goal is to determine how helpful each review is in assisting a customer in deciding whether to purchase a product. Included below are details about a product called META and a set of reference reviews of the same product with human-provided scores indicating their usefulness. Utilize these reference reviews in understanding in calculating the helpfulness of the reviews. Also use the criteria and scoring rubric, drawing from literature on review helpfulness and user perception.

META:

Product Name	: `<Product Name>`
Product Description: `<Product Description>`
About the Product :  `<About the Product>`

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
The following are a set of reviews of the same product which are human labelled.
Each object contains the following fields:

1. "rating": The star rating given by the customer.
2. "title": The title of the review.
3. "text": The actual review text.
4. “helpfulness” : This is the human assigned score for the review based on how helpful the review is.

The reference reviews are : `<Reference Reviews>`
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

Please now rate the following reviews:
`<Review List>`
