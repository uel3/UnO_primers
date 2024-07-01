import sys

def find_keys_with_values(dictionaries, target_values):
    matching_keys = []

    for dictionary in dictionaries:
        for key, values in dictionary.items():
            if all(value in values for value in target_values):
                matching_keys.append(key)

    return matching_keys

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.txt")
        return

    input_file = sys.argv[1]
    output_file = "primers_in_all_rep_species.txt"  # Set the output file name here

    with open(input_file, "r") as file:
        lines = file.readlines()

    dictionaries = []
    for line in lines:
        key, values_str = line.strip().split(":")
        values = [value.strip("' ") for value in values_str.strip(" []").split(",")]
        dictionaries.append({key: values})

    target_values = {'1143560907', '749310542', '749314519', '1004367656', '1133548812', '983532915', '1151114342', '58156'}  # Note: Using strings as values

    matching_keys = find_keys_with_values(dictionaries, target_values)

    with open(output_file, "w") as outfile:
        for key in matching_keys:
            outfile.write(key + "\n")

if __name__ == "__main__":
    main()
