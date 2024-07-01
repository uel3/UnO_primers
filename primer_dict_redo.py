import sys

# List of valid prefixes for fasta names
valid_prefixes = ["1143560907", "749310542", "749314519", "1004367656", "1133548812", "983532915", "1151114342", "58156"]  # These are salmonella fasta file names

# Initialize an empty dictionary to store the data
primer_fasta_dict_with_desired_prefixes = {}

# Get the input file path from the command line arguments
if len(sys.argv) != 2:
    print("Usage: python script.py input_file.txt")
    sys.exit(1)

input_file_path = sys.argv[1]

# Read the file line by line
with open(input_file_path, 'r') as file:
    for line in file:
        # Split the line into columns using comma as the separator
        columns = line.strip().split(',')  # Adjust the separator if needed

        # Ensure the line has at least 3 columns
        if len(columns) >= 3:
            primer_name = columns[1]  # Primer name is the second column
            fasta_name = columns[2]  # Fasta name is the third column

            # Check if the primer_name already exists in the dictionary
            if primer_name in primer_fasta_dict_with_desired_prefixes:
                primer_fasta_dict_with_desired_prefixes[primer_name].append(fasta_name)
            else:
                primer_fasta_dict_with_desired_prefixes[primer_name] = [fasta_name]

# Filter primer names with at least one desired prefix in their associated fasta names
filtered_dict = {}
for primer, fasta_list in primer_fasta_dict_with_desired_prefixes.items():
    if all(fasta.startswith(tuple(valid_prefixes)) for fasta in fasta_list):
        filtered_dict[primer] = fasta_list

# Write the dictionaries to the output file
with open('primer_fasta_with_desired_prefixes.txt', 'w') as file:
    for primer, fasta_list in filtered_dict.items():
        file.write(f"{primer}: {fasta_list}\n")
