# assignment 1303

## Data checking for head pose, eye gaze and emotions 

### To start:
change the ````input_file_path```` and ````output_file_path````


#### Features  
Reading Input Data:  
The script reads input data from a file, where each line represents a JSON object containing information about head pose, eye gaze, and emotions.  

Data Cleaning: The raw data is cleaned and validated by checking if the required fields exist and whether the values are of the correct type (e.g., float for numeric values).
Attention Value Calculation: For each valid entry, the script calculates an attention value based on head pose stability, eye alignment, and emotional state.


Dominant Emotion: The script determines the dominant emotion from the data (happy, sad, angry, neutral, or other).
Sorting and Output: The processed data is sorted by attention value in descending order, and the results are written to an output file in a readable format.
Error Handling: The script dynamically tracks and records any errors encountered during data reading or processing.

