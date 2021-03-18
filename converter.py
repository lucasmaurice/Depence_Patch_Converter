import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import ntpath

# ===============================================
# ==================== Tools ====================
# ===============================================

# Export a value from a dict, with a default value if missing.
# Print a warning on the first time the missing value is found
missing_parameters = []


def get_key(the_dict, the_key, default="0"):
    global missing_parameters
    if the_key not in the_dict:
        if the_key not in missing_parameters:
            missing_parameters.append(the_key)
            print("WARNING: The key \"" + the_key + "\" is missing. Will default to `" + str(default) + "`.")
        return default
    return the_dict[the_key]


# ==============================================
# ==================== Main ====================
# ==============================================

# Init TkInter for file selection window
Tk().withdraw()
# Open file selection windows
input_file_path = askopenfilename()
print("Will open `" + input_file_path + "`")

# Generate output file path
head, tail = ntpath.split(input_file_path)
output_file_path = head + '/output.csv'
print("Will save as `" + output_file_path + "`")

# Open input and output file
with open(input_file_path, newline='') as input_file:
    with open(output_file_path, 'w', newline='') as output_file:
        # Generate Headers
        fieldnames = ['Spot', 'Type', 'Patch', 'X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ', 'Position', 'Channel', 'Layer', 'Purpose', 'Focus', 'Color', 'Gobo']

        # Write Headers
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        # Read fixture list
        fixtures_list = csv.DictReader(input_file)
        for fixture in fixtures_list:

            # Write new fixture line in output file
            writer.writerow({
                    'Spot': fixture["Fixture ID"],
                    'Patch': fixture["DMX Line"] + '.' + fixture["DMX Address"],
                    'Type': fixture["Name"],
                    'X': str(float(get_key(fixture, "X Pos")) / 100) + 'm',
                    'Y': str(float(get_key(fixture, "Z Pos")) / 100) + 'm',
                    'Z': str(float(get_key(fixture, "Y Pos")) / 100) + 'm',
                    'RotX': get_key(fixture, "X Rotation"),
                    'RotY': get_key(fixture, "Z Rotation"),
                    'RotZ': get_key(fixture, "Y Rotation"),
                })
