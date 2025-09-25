#!/usr/bin/env python

import csv
import pandas as pd

def hms_to_ms(hms_string):
    """
    Converts a time string in 'hh:mm:ss', 'mm:ss', or 'ss' format to milliseconds.
    """
    try:
        # print(hms_string)  # Debugging line to check the input format
        if hms_string is None or hms_string.strip() == '':
            return None

        parts = list(map(int, hms_string.split(':')))
        
        # Determine the number of parts to handle different formats
        if len(parts) == 3:
            h, m, s = parts
        elif len(parts) == 2:
            h, m, s = 0, parts[0], parts[1]
        elif len(parts) == 1:
            h, m, s = 0, 0, parts[0]
        else:
            raise ValueError("Time format must be hh:mm:ss, mm:ss, or ss")

        # Calculate total milliseconds
        return (h * 3600 + m * 60 + s) * 1000
    except (ValueError, IndexError):
        raise ValueError("Invalid time format. Please use hh:mm:ss, mm:ss, or ss.")


def save_as_csv(csv_path, data):
    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)


def save_dict_as_csv(csv_path, data):
    # Create the DataFrame
    df = pd.DataFrame(data)

    # save the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)