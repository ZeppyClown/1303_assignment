import unittest

from assignment import read_input_file, isFloat, calculate_attention_value, get_dominant_emotion, process_and_sort_data, \
    write_output_file, clean_data


class test(unittest.TestCase):

        def test_clean_data(self):
                # Test cleaning valid data
                raw_data = ['{"head_pose": {"pitch": 10, "yaw": 20}, "eye_gaze": {"pitch": 15, "yaw": 25}, "emotions": {"happy": 0.4, "sad": 0.2, "angry": 0.1, "neutral": 0.3}}']
                cleaned = clean_data(raw_data)
                self.assertEqual(len(cleaned), 1)  # Expect one valid entry

                # Test invalid JSON input
                raw_data = ['invalid json string']
                cleaned = clean_data(raw_data)
                # Expect 0 valid entries
                self.assertEqual(len(cleaned), 0)


        def test_isFloat(self):
            # Test valid floats
            valid_data = {
                "head_pose": {"pitch": "10.0", "yaw": "5.5"},
                "eye_gaze": {"pitch": "12.1", "yaw": "8.0"},
                "emotions": {"happy": "0.5", "sad": "0.2", "angry": "0.1", "neutral": "0.2"}
            }
            self.assertTrue(isFloat(valid_data, "head_pose", "pitch"))
            self.assertTrue(isFloat(valid_data, "emotions", "happy"))

            # Test invalid float value
            invalid_data = {
                "head_pose": {"pitch": "not_a_number", "yaw": "5.5"},
                "eye_gaze": {"pitch": "invalid", "yaw": "8.0"}
            }
            try:
                check = isFloat(invalid_data, "head_pose", "pitch")
            except Exception as e:
                check = False
            self.assertFalse(check)

        def test_calculate_attention_value(self):
            # Test valid data
            head_pose = {"pitch": 10, "yaw": 20}
            eye_gaze = {"pitch": 15, "yaw": 25}
            emotions = {"emotions": {"happy": 0.4, "sad": 0.2, "angry": 0.1, "neutral": 0.3}}
            result = calculate_attention_value(head_pose, eye_gaze, emotions)
            print(result)
            self.assertAlmostEqual(result, 0.78, places=2)

        def test_get_dominant_emotion(self):
            # Test happy as the dominant emotion
            emotions = {"emotions": {"happy": 0.5, "sad": 0.1, "angry": 0.1, "neutral": 0.3}}
            result = get_dominant_emotion(emotions)
            self.assertEqual(result, "Happy")

            # Test other emotion as the dominant emotion
            emotions = {"emotions": {"confused": 0.6, "bored": 0.4}}
            result = get_dominant_emotion(emotions)
            self.assertEqual(result, "Other")

        def test_process_and_sort_data(self):
            # Test processing and sorting
            cleaned_data = [
                {"head_pose": {"pitch": 10, "yaw": 20}, "eye_gaze": {"pitch": 15, "yaw": 25}, "emotions": {"happy": 0.4, "sad": 0.2, "angry": 0.1, "neutral": 0.3}},
                {"head_pose": {"pitch": 5, "yaw": 10}, "eye_gaze": {"pitch": 8, "yaw": 12}, "emotions": {"happy": 0.6, "sad": 0.1, "angry": 0.1, "neutral": 0.2}}
            ]
            sorted_data = process_and_sort_data(cleaned_data)
            # Test that the data is sorted by "Attention Value" in descending order
            self.assertGreater(sorted_data[0]["Attention Value"], sorted_data[1]["Attention Value"])

if __name__ == "__main__":
    unittest.main()
    test_file = "test_data.txt"



