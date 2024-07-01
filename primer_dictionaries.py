import sys

def create_dictionaries(input_file):
    fasta_dict = {}

    with open(input_file, "r") as file:
        for line in file:
            seqid, primer_name, fasta_name = line.strip().split(",")
            if fasta_name not in fasta_dict:
                fasta_dict[fasta_name] = []
            fasta_dict[fasta_name].append(primer_name)

    return fasta_dict

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.txt")
        return

    input_file = sys.argv[1]
    fasta_dict = create_dictionaries(input_file)

    with open("fasta_primer_dictionary.txt", "w") as output_file:
        for fasta_name, primer_names in fasta_dict.items():
            output_file.write(f"Fasta Name: {fasta_name}\n")
            output_file.write(f"  Primer Names: {', '.join(primer_names)}\n")

if __name__ == "__main__":
    main()
