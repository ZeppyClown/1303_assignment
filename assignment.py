import json
import math

found_errors = {}


def read_input_file(file_path: str) -> list[str]:
    """
    Reads the input data file line by line and returns the raw data as a list of strings.
    
    Args:
    file_path (str): The path to the input data file.

    Returns:
    list[str]: A list of strings, each representing a line of data from the input file.

    Raises:
    FileNotFoundError: If the specified file path does not exist.
    Exception: For other potential file I/O errors.
    """
    # Put your code here
    lines = []
    f = open(file_path, "r")
    line = f.readline()
    while line:
        line = line.rstrip()
        lines.append(line)
        line = f.readline()
    return lines



def clean_data(raw_data: list[str]) -> list[dict]:
    """
    Cleans raw data by converting each JSON string to a dictionary
    and checking for the presence of required keys and valid data types.
    *Note: each entry of the data should at least contain these 4 emotion values: happy, sad, angry, neutral

    Args:
    raw_data (list[str]): A list of JSON strings representing the raw data.

    Returns:
    list[dict]: A list of dictionaries containing valid data entries.
    """
    # Put your code here

    data_dict = []
    i = 0
    while i < len(raw_data):
        try:
            temp_dict= json.loads(raw_data[i])
            if isNumber(temp_dict, "head_pose", "pitch") and isNumber(temp_dict, "head_pose", "yaw") and isNumber(temp_dict, "eye_gaze", "pitch") and isNumber(temp_dict, "eye_gaze", "yaw") and isNumber(temp_dict, "emotions", "happy") and isNumber(temp_dict, "emotions", "sad") and isNumber(temp_dict, "emotions", "angry")and isNumber(temp_dict, "emotions", "neutral"):
                data_dict.append(temp_dict)

        except Exception as error:
            add_error_type(type(error).__name__)
        i += 1

    return data_dict
def isNumber(dict: list[dict],outer: str, inner: str):
    if isinstance(dict[outer][inner], (int, float)):
        return True
    else:
        add_error_type("TypeError")
        return False



    
def add_error_type(error_name, error_count=1):
    """
    Records the occurrence of a specific error type.
    
    Parameters:
    - error_name (str): The name of the error to record.
    - error_count (int, optional): The number of times this error occurred. Defaults to 1.
    
    If the error type is not already in the found_errors dictionary, it initializes the count at 0.
    Then, it increments the count of the specified error by the given error_count.
    """
    if error_name not in found_errors:
        found_errors[error_name] = 0
    found_errors[error_name] += error_count

    print(found_errors)

    
def print_data_errors():
    """
    Prints a summary of all recorded errors.
    
    If there are any errors recorded in the found_errors dictionary, it generates a summary string
    that lists each error type and its count, followed by the total number of errors.
    If no errors are recorded, it prints "Found 0 Error".
    """
    if len(found_errors) > 0:
        s, t = "", 0
        for k, v in found_errors.items():
            s += f"{k}:{v};"
            t += v
        s = f"Found {t} errors -> ({s})"
        print(s)
    else:
        print("Found 0 Error")


def calculate_attention_value(head_pose: dict, eye_gaze: dict, emotions: dict) -> float:
     """
        Calculates the attention value based on head pose, eye gaze, and emotions.
        The attention value is a weighted sum of head stability, eye alignment, and emotion influence.

        Args:
        head_pose (dict): Dictionary containing head pose data with keys 'pitch' and 'yaw'.
        eye_gaze (dict): Dictionary containing eye gaze data with keys 'pitch' and 'yaw'.
        emotions (dict): Dictionary containing emotion probabilities.

        Returns:
        float: The calculated attention value rounded to two decimal places.
        """
     #Put your code here
     head_stability = max(0.0, (1 - (
                 (math.fabs(head_pose["pitch"]) + math.fabs(head_pose["yaw"])) / 180)))

     eye_alignment = max(0.0, (1 -(
                 (math.fabs(eye_gaze["pitch"] - head_pose["pitch"]) +
                 (math.fabs(eye_gaze["yaw"] - head_pose["yaw"]))) / 180)))

     emotion_score = float((emotions["emotions"]["happy"]) + (emotions["emotions"]["neutral"]) - (emotions["emotions"]["sad"]) - (emotions["emotions"]["angry"]))

     emotion_value = float((0.5 * head_stability) + (0.3 * eye_alignment) + (0.2 * emotion_score))
     return round(emotion_value, 2)



def get_dominant_emotion(emotions: dict) -> str:
    """
    Determines the dominant emotion based on the highest probability value in the emotions dictionary.

    Args:
    emotions (dict): Dictionary containing emotion probabilities.

    Returns:
    str: The emotion with the highest probability. The value should be one in this set: [“Happy”, “Neutral”, “Sad”, “Angry”, “Other”]
    """
    # Put your code here
    # just get the highest emotion value


    dominant_emotion = max(emotions["emotions"], key=emotions["emotions"].get)

    if (dominant_emotion == "happy" or dominant_emotion == "neutral" or dominant_emotion == "sad" or  dominant_emotion == "angry" ):
        dominant_emotion = dominant_emotion[0].upper() + dominant_emotion[1:]
        return dominant_emotion
    else:
        return "Other"
# hi





        
def process_and_sort_data(cleaned_data: list[dict]) -> list[dict]:
    """
    Processes cleaned data to calculate attention values, determine dominant emotions,
    and sort the entries by attention value in descending order.

    Args:
    cleaned_data (list[dict]): A list of dictionaries containing valid data entries.

    Returns:
    list[dict]: A list of processed and sorted data entries with attention values and dominant emotions.
    """
    results = process_data(cleaned_data)
    
    # Sort results by attention value in descending order
    results.sort(key=lambda x: x["Attention Value"], reverse=True)
    return results


def process_data(cleaned_data: list[dict]) -> list[dict]:
    """
    Processes cleaned data to calculate attention values, determine dominant emotions.

    Args:
    cleaned_data (list[dict]): A list of dictionaries containing valid data entries.

    Returns:
    list[dict]: A list of processed data entries with attention values and dominant emotions.
    """
    # Put your code here
    # call get dominant emotion
    # call the for loop here
    final_results = []
    i = 0
    for x in cleaned_data:
        dominant_emotion = get_dominant_emotion(x)
        attention_value = calculate_attention_value(x["head_pose"], x["eye_gaze"], x)
        final_results.append({
            "Attention Value": attention_value,
            "Head Pose": x["head_pose"],
            "Eye Gaze": x["eye_gaze"],
            "Dominant Emotion": dominant_emotion
        })
    return final_results


def write_output_file(results: list[dict], file_path: str):
    """
    Writes the processed and sorted data to an output file, formatting each entry for readability.

    Args:
    results (list[dict]): A list of processed data entries with attention values and dominant emotions.
    file_path (str): The path to the output file where results will be saved.

    Raises:
    Exception: For potential file I/O errors during the write operation.
    """
    # Put your code here

    # Assuming `results` is a list of dictionaries
    with open('output.txt', 'w') as file:
        for result in results:
            # Create the formatted string
            formatted_output = (
                f"Attention Value: {result['Attention Value']} | Head Pose: Pitch {result['Head Pose']['pitch']}, "
                f"Yaw {result['Head Pose']['yaw']} | Eye Gaze: Pitch {result['Eye Gaze']['pitch']}, "
                f"Yaw {result['Eye Gaze']['yaw']} | Dominant Emotion: {result['Dominant Emotion']}")
            # Write the formatted string to the file
            file.write(formatted_output + '\n')  # Add a newline after each entry


def main():
    """
    Main function that orchestrates the workflow of reading input data, cleaning and processing it,
    calculating attention values, determining dominant emotions, sorting the results, and writing them to an output file.
    """
    input_file_path = "attention_data.txt"
    output_file_path = "attention_results.txt"

    raw_data = read_input_file(input_file_path)
    cleaned_data = clean_data(raw_data)
    sorted_results = process_and_sort_data(cleaned_data)
    write_output_file(sorted_results, output_file_path)

    print(f"Processing complete. Results saved to {output_file_path}.")

if __name__ == "__main__":
    main()
