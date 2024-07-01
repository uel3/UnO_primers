import sys
from collections import defaultdict, Counter

def normalize_primer_name(primer_name):
    return primer_name.strip().replace("Primer Names: ", "")

def count_primer_frequencies(input_file):
    primer_frequencies = Counter()
    primer_occurrences = defaultdict(set)
    fasta_associations = defaultdict(set)
    all_fasta_names = set()

    with open(input_file, "r") as file:
        lines = file.readlines()
        fasta_name = None

        for line in lines:
            if line.startswith("Fasta Name: "):
                fasta_name = line.strip().replace("Fasta Name: ", "")
                all_fasta_names.add(fasta_name)
            elif fasta_name and line.startswith("  Primer Names: "):
                primer_names = line.strip().replace("  Primer Names: ", "").split(", ")
                primer_names = [normalize_primer_name(primer) for primer in primer_names]
                primer_frequencies.update(primer_names)
                for primer_name in primer_names:
                    primer_occurrences[primer_name].add(fasta_name)
                    fasta_associations[primer_name].add(fasta_name)

    return primer_frequencies, primer_occurrences, fasta_associations, all_fasta_names

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 no_matches.py fasta_primer_dictionary.txt")
        return

    input_file = sys.argv[1]
    primer_frequencies, primer_occurrences, fasta_associations, all_fasta_names = count_primer_frequencies(input_file)

    for primer_name, frequency in primer_frequencies.items():
        occurrence_count = len(primer_occurrences[primer_name])
        print(f"Primer Name: {primer_name}, Frequency: {frequency}, Occurrences: {occurrence_count}")

    print("\nFasta names not associated with each individual primer:")
    for primer_name in primer_frequencies:
        unused_fasta_files = all_fasta_names - fasta_associations[primer_name]
        if unused_fasta_files:
            print(f"Primer Name: {primer_name}")
            for fasta in unused_fasta_files:
                print(f"  {fasta}")

if __name__ == "__main__":
    main()
