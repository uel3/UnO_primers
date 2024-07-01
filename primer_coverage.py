import sys
from collections import defaultdict, Counter

def normalize_primer_name(primer_name):
    return primer_name.strip().replace("Primer Names: ", "") #this makes primer names consistent and does not results in duplicates

def count_primer_frequencies(input_file):
    primer_frequencies = Counter()
    primer_occurrences = defaultdict(set)

    with open(input_file, "r") as file:
        lines = file.readlines()
        fasta_name = None

        for line in lines:
            if line.startswith("Fasta Name: "):
                fasta_name = line.strip().replace("Fasta Name: ", "")
            elif fasta_name and line.startswith("  Primer Names: "):
                primer_names = line.strip().replace("  Primer Names: ", "").split(", ")
                primer_names = [normalize_primer_name(primer_name) for primer_name in primer_names]
                primer_frequencies.update(primer_names)
                for primer_name in primer_names:
                    primer_occurrences[primer_name].add(fasta_name)

    return primer_frequencies, primer_occurrences

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 primer_coverage.py fasta_primer_dictionary.txt")
        return

    input_file = sys.argv[1]
    primer_frequencies, primer_occurrences = count_primer_frequencies(input_file)
    total_fasta_names = len(set(fasta_name for fasta_names in primer_occurrences.values() for fasta_name in fasta_names))

    for primer_name, frequency in primer_frequencies.items():
        occurrence_count = len(primer_occurrences[primer_name])
        coverage_percentage = (occurrence_count / total_fasta_names) * 100
        print(f"Primer Name: {primer_name}, Frequency: {frequency}, Coverage: {coverage_percentage:.2f}%")  #coverage is based on the number of fasta names or seq_ids that had ampliccons generated, if not all then the max value is based on the number of seq_ids that had amplicons

if __name__ == "__main__":
    main()
