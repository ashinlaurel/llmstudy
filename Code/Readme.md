# Code Readme

Inside each category folder: 
zero_shot.py : Runs zero shot prompt for the particular category product
The corresponding helpfulness ratings given by LLM will be present inside 
./<model_name>/zero_shot/ folder. 

zero_shot_post_process.py : Compares the human ratings and LLM ratings.
Stores the result(RMSE, MAE, etc.) in file ./zero_shot_output.txt. 

finetune_1.py : Runs few shot prompt for the particular category product
The corresponding helpfulness ratings given by LLM will be present inside 
./<model_name>/finetune/ folder. 

finetune_1_post_process.py : Compares the human ratings and LLM ratings.
Stores the result(RMSE, MAE, etc.) in file ./finetune_output.txt. 

finetune_2.py : Runs few shot prompt (with the product's own examples) 
for the particular category product. The corresponding helpfulness ratings 
given by LLM will be present inside  ./<model_name>/finetune_2/ folder.

finetune_2_post_process.py : Compares the human ratings and LLM ratings.
Stores the result(RMSE, MAE, etc.) in file ./finetune_2_output.txt. 
