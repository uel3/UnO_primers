import sys

valid_prefixes = ["1143560907", "749310542", "749314519", "1004367656", "1133548812", "983532915", "1151114342", "58156"]  # # List of valid_prefixes for fasta names, these are salmonella fasta file names

primer_fasta_dict_with_desired_prefixes = {}

if len(sys.argv) != 2:
    print("Usage: python3 primer_dict_redo.py concatonated_files.txt") 
    sys.exit(1)

input_file_path = sys.argv[1]

with open(input_file_path, 'r') as file:
    for line in file:
        columns = line.strip().split(',') 

        
        if len(columns) >= 3: # Ensure input formatting is correct
            primer_name = columns[1]  # Primer name is second column
            fasta_name = columns[2]  # Fasta name is third column

            
            if primer_name in primer_fasta_dict_with_desired_prefixes:
                primer_fasta_dict_with_desired_prefixes[primer_name].append(fasta_name)
            else:
                primer_fasta_dict_with_desired_prefixes[primer_name] = [fasta_name]


filtered_dict = {} # Filter primer names with at least one desired prefix in their associated fasta names
for primer, fasta_list in primer_fasta_dict_with_desired_prefixes.items():
    if all(fasta.startswith(tuple(valid_prefixes)) for fasta in fasta_list):
        filtered_dict[primer] = fasta_list

with open('primer_fasta_with_desired_prefixes.txt', 'w') as file:
    for primer, fasta_list in filtered_dict.items():
        file.write(f"{primer}: {fasta_list}\n")
