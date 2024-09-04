
You are a data scientist who is trying to analyze the usefulness of reviews in eccomerce platforms. You are trying to find how helpful a review is in helping the customer decide whether to buy the product or not. Consider factors such as the level of detail, specificity, and the relevance of the information provided. If similar reviews are present, score them separately and ignore that they were similar.

When rating reviews, apply these criteria systematically:
- Examine the review's content for specificity and detail.
- Consider the review's length and ensure it strikes a balance between being thorough and concise.
- Check the credibility of the reviewer, focusing on verified purchases and expertise.
- Look for a balanced perspective that includes both pros and cons.
- Evaluate the sentiment for constructiveness and neutrality.*
- Ensure the review is readable and well-written.
- Value comparative insights provided by the reviewer.

Input:
A JSON array with multiple objects is provided representing user reviews of a product from amazon. Each object contains the following fields:
1. "review_id" (a unique identifier for the review),
2. "rating" (the star rating given by the user)
3. "title" (the title of the review)
4. "text" (the actual review text).
Task:
Evaluate each review and assign a helpfulness score from 1-5 on how helpful the review will be. Follow the following output format strictly.

Output:
Return a json array under key "Reviews". It should have the following fields:
1. "helpfulness" : helpfulness score
2. "review_id": review_id of the review
3.   "reason" : reasoning for why the score was given
 Do not add any other fields.


# Prompt 3

You are a data scientist who is analyzing the usefulness of reviews on e-commerce platforms. Your goal is to determine how helpful each review is in assisting a customer to decide whether to purchase a product. Consider factors such as the level of detail, specificity, and relevance of the information provided.

Criteria for Rating Reviews
When rating reviews, apply the following criteria systematically:
- Examine the review's content for specificity and detail.
- Consider the review's length and ensure it strikes a balance between being thorough and concise.
- Check the credibility of the reviewer, focusing on verified purchases and expertise.
- Look for a balanced perspective that includes both pros and cons.
- Evaluate the sentiment for constructiveness and neutrality.*
- Ensure the review is readable and well-written.
- Value comparative insights provided by the reviewer.

Rubric Scoring

When rating reviews, apply the following criteria systematically. Each criterion is rated on a scale from 1 to 5, where:

- **1**: Very poor
- **2**: Poor
- **3**: Average
- **4**: Good
- **5**: Excellent

1. **Specificity and Detail**:

    - 1: Lacks detail, very vague.
    - 2: Some detail but still vague.
    - 3: Provides adequate detail.
    - 4: Detailed and specific.
    - 5: Extremely detailed and specific.
2. **Length and Conciseness**:

    - 1: Too short to be useful or excessively long.
    - 2: Somewhat short or somewhat long.
    - 3: Appropriate length but could be more concise.
    - 4: Good balance of thoroughness and conciseness.
    - 5: Perfect balance, very thorough and concise.
3. **Reviewer Credibility**:

    - 1: No indication of credibility.
    - 2: Slight indication of credibility.
    - 3: Moderately credible
    - 4: Credible with good indications of expertise.
    - 5: Highly credible
4. **Balanced Perspective**:

    - 1: Extremely biased.
    - 2: Mostly biased.
    - 3: Somewhat balanced but still biased.
    - 4: Balanced with both pros and cons.
    - 5: Very balanced and unbiased.
5. **Constructive Sentiment**:

    - 1: Highly emotional, not constructive.
    - 2: Somewhat emotional.
    - 3: Moderately constructive.
    - 4: Mostly constructive and neutral.
    - 5: Highly constructive and neutral.
6. **Readability**:

    - 1: Very difficult to read.
    - 2: Somewhat difficult to read.
    - 3: Readable but with some issues.
    - 4: Easy to read and well-written.
    - 5: Extremely clear and very well-written.
7. **Comparative Insights**:

    - 1: No comparative insights.
    - 2: Very few comparative insights.
    - 3: Some comparative insights.
    - 4: Good comparative insights.
    - 5: Excellent comparative insights.

Final Scoring
Assign a helpfulness score from 1-5 based on the average score across all criterias provided above.

Input
You will receive a JSON array with multiple objects representing user reviews of a product from Amazon. Each object contains the following fields:
1. "review_id": A unique identifier for the review.
2. "rating": The star rating given by the user.
3. "title": The title of the review.
4. "text": The actual review text.

Output
Return a JSON array under the key "Reviews". Each object in the array should contain the following fields:
1. "helpfulness": Helpfulness score (1-5).
2. "review_id": The review_id of the review.
3. "reason": Reasoning for why the score was given.

Example Output
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

Task
Evaluate each review and assign a helpfulness score from 1-5 based on the criteria provided. Follow the output format strictly.

Notes
- Score each review individually, regardless of similarity to other reviews.
- Provide clear and concise reasoning for each score assigned.





# Key Factors
Certainly! Here are the additional key factors for rating reviews:

### Key Factors for Rating Reviews

1. **Specificity and Detail**: Look for reviews that provide detailed and specific information about the product. Chevalier and Mayzlin (2006) found that detailed reviews significantly impact sales, indicating their value. Reviews should mention specific features, benefits, and drawbacks, as well as usage experiences.

2. **Length and Depth**: According to Mudambi and Schuff (2010), moderately long reviews are often more helpful. They provide enough detail to be informative but are concise enough to maintain the reader’s attention.

3. **Balanced Perspective**: Useful reviews often present both positive and negative aspects of the product. This balanced approach, highlighted by Baek, Ahn, and Choi (2012), provides a more comprehensive view, helping potential buyers make informed decisions.

4. **Constructive Sentiment**: Reviews that contain constructive criticism rather than purely emotional responses tend to be more helpful. Yin, Bond, and Zhang (2014) noted that reviews expressing discrete emotions like anxiety or anger could affect perceived helpfulness differently, with more neutral and balanced sentiments being preferred.

5. **Readability and Language**: Reviews that are well-written, easy to read, and free from grammatical errors are more likely to be useful (Korfiatis, García-Bariocanal, & Sánchez-Alonso, 2012). Look for clear, concise, and coherent language.

6. **Comparative Insights**: Reviews that compare the product with similar items can provide valuable context and help in understanding its relative advantages or disadvantages (Pan, 2012).

7. **Emotionally Intelligent Language**: Reviews that use emotionally intelligent language, acknowledging the reviewer’s feelings and perspectives without being overly emotional or biased, tend to be more helpful. This aligns with the findings of Ghose and Ipeirotis (2011) that emotionally intelligent reviews can enhance trustworthiness and perceived helpfulness.

8. **Relevance to the Product**: Reviews that are relevant to the product and address its specific features and intended use are more useful. According to Hu, Liu, and Zhang (2008), the relevance of the review content to the product significantly impacts its perceived helpfulness.

9. **Use of Evidence**: Reviews that include evidence, such as photos, videos, or specific examples, can be more convincing and helpful. Chen, Samaranayake, Cen, Qi, and Lan (2014) found that reviews backed by concrete evidence are perceived as more credible and informative.

10. **User Experience Context**: Reviews that provide context about the user’s experience, such as their background or specific use case, can help others with similar contexts make better decisions. Lackermair, Kailer, and Kanmaz (2013) emphasized the importance of understanding the context in which the product was used to gauge the review’s relevance.

11. **Consistency with Rating**: Reviews that are consistent with the given rating are more reliable. Inconsistencies between the text and the star rating can confuse potential buyers. Chen, Dhanasobhon, and Smith (2008) noted that consistency between the review content and the rating enhances the review’s credibility and usefulness.

### References
1. Chevalier, J. A., & Mayzlin, D. (2006).
2. Mudambi, S. M., & Schuff, D. (2010).
3. Hu, N., Liu, L., & Zhang, J. J. (2008).
4. Baek, H., Ahn, J., & Choi, Y. (2012).
5. Yin, D., Bond, S. D., & Zhang, H. (2014).
6. Korfiatis, N., García-Bariocanal, E., & Sánchez-Alonso, S. (2012).
7. Pan, Y. (2012).
8. Ghose, A., & Ipeirotis, P. G. (2011).
9. Lackermair, G., Kailer, D., & Kanmaz, K. (2013).
10. Chen, T., Samaranayake, P., Cen, X., Qi, M., & Lan, Y. (2014).
11. Chen, P., Dhanasobhon, S., & Smith, M. (2008).



Length -> biased towards the higher side
comparitive -> tell it about comparision with other products
