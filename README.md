## UnO_primers

This is a collection of scripts used to parse potential UnO primers for Salmonella from MRI Global

A. Before beginning these steps, primer files should be in the following tab seperated format: primer_name   forward_primer_sequence reverse_primer_seqeunce
```bash
nontyphi_nucl_18mers_sam_0_FR	TACCAATTCCGCCACCTTCG	CGAAGGTGGCGGAATTGGTA
nontyphi_nucl_18mers_sam_1_FR	ACTTCTGAGTTCGGCATGGG	CCCATGCCGAACTCAGAAGT
Paratyphi_ABC_18mer_nucl_sam_86_FR	GGACGGTCGCTACATCAACA	CGGTTCGATGTTCATGGTGC
```
See (https://github.com/uel3/UnO_primers/blob/main/primers.txt) for an example primer file

## Requirements for using these scripts
Follow the download instructions to use the repo (https://github.com/uel3/HMAS-QC-Pipeline_UnO)
This is branched from (https://github.com/ncezid-biome/HMAS-QC-Pipeline) developed by [@jessicarowell](https://github.com/jessicarowell) and [@jinfinance](https://github.com/jinfinance) witerrh additional error handling
The UnO_params branch contains the script with the UnO amplicon parameters (https://github.com/uel3/HMAS-QC-Pipeline_UnO/tree/UnO_params)

The parameters are :
```bash
mismatch_percent = 6
min_amplicon_len = 100
max_amplicon_len = 500
max_seqid_len = 50
```


Python3 is required for both HMAS-QC-Pipeline and the following parsing scripts Download python [here](https://www.python.org/downloads/)

## Using the scripts
1. Run candidate primers against database of choice, which in this case is folder of stool genomes in fasta format
```bash
$ python3 ~/HMAS-QC-Pipeline/extract_amplicon_from_primersearch_output_UnO.py -s path/to/folder/with/database/genomes -p path/to/formatted/primers.txt
```
This will output all output files from running HMAS-QC-Pipeline/extract_amplicon_from_primersearch_output_UnO.py. There are 4 files:
fasta_extractedAmplicons.fasta
fasta_metasheet.csv
fasta_not_match_primers.txt
fasta.ps

2. Concatenate all metasheet.csv files greater than 21 bytes, any metasheet.csv file less than 21 bytes is empty, meaning no amplicons were generated 
```bash
$ find . -type f -name "*meta*" -size +21c | while read -r file; do tail -n +2 "$file"; done > concatenated_file.txt
```
3. primer_dict_redo.py will create a dictionary of the primers for the bug specific seq_ids or fasta names in which they generate the amplicons
```bash
$ python3 primer_dict_redo.py concatenated_files.txt 
```
Output generated from this script: primer_fasta_with_desired_prefixes.txt which contains only primers that generate amplicons in any Salmonella from "valid_prefixes". This will need to be modified depending on which stool genomes from which you are trying generate amplicons.

4. Use new_extract_primer_names.py to identify primers that generate amplicons in all Salmonella from primer_dict_redo.py output primer_fasta_with_desired_prefixes.txt
```bash
$ python3 new_extract_primer_names.py primer_fasta_with_desired_prefixes.txt
```
Output generated from this script: primers_in_all_rep_species.txt will contain only the primer names of the primers that only generate amplicons in Salmonella and in all Salmonella found in "tagert_values". This will need to be modified depending on which stool genomes from which you are trying generate amplicons.


5. Using grep and the output from new_extract_primer_names.py, primers_in_all_rep_species.txt, we create a new primer file from the original primer file to limit our candidate primers to those that only generate amplicons in Salmonella and generate amplicons in all Salmonella
```bash
$ grep -f primers_in_all_rep_species.txt primers.txt > secondary_test_primers.txt
```
6. To identify the breadth of the candidate primers, use the secondary_test_primers.txt to check amplicons in a bug specific database
```bash
$ python3 ~/HMAS-QC-Pipeline/extract_amplicon_from_primersearch_output_UnO.py -s path/to/bug/specific/database/genomes-p ~path/to/primer_file/secondary_test_primers.txt
```
7. Concatenate all non-empty metasheet.csv to generate a list of seq_id,primer,sample for all primers that generated amplicons
```bash
$ find . -type f -name "*meta*" -size +21c | while read -r file; do tail -n +2 "$file"; done > concatenated_file_secondary.txt
```
8. In order to evaluate the breadth of amplcions generated by the candidate primers, use primer_dictionaries.py to create a dictionary to generate various statistics
```bash
$ python3 primer_dictionaries.py concatenated_file_secondary.txt
```
9. primer_coverage.py will generate coverage statistics of the bug specific database, frequency is the number of amplicons that are generated by that primer in the bug specific database, coverage is the percentage of amplicons generated in the bug specific database
```bash
$ python3 primer_coverage.py fasta_primer_dictionary.txt
```
```shell
Primer Name: primer_1, Frequency: 262, Coverage: 98.50%
Primer Name: primer_2, Frequency: 227, Coverage: 85.34%
Primer Name: primer_3, Frequency: 266, Coverage: 100.00%
```
10. not_matches.py takes fasta_primer_dictionary.txt as input and will generate the same stats as primer_coverage.py but also which seq_ids from the bug specfic database that do not have amplicons generated by the candidate primers. It's worth noting the coverage calculations is dependent on the maximum number of fasta names. If amplicons are not generated in all fasta names from the bug specific database, the coverage calculation will be based on the maximum number of fasta names that result in amplicons. For example, if a bug specific databse contains 266 fasta names/seq_ids, only 260 have amplicons generated by the candidate primers, coverage calulations will be out of 260 instead of 266. The not_matches.py script will also only tell you the fasta names/seq_ids that do not generate amplicons from the 260 fasta names and not the 266. 
```bash
$ python3 not_matches.py fasta_primer_dictionary.txt
```
```shell
Primer Name: primer_1, Frequency: 262, Coverage: 98.50%
Primer Name: primer_3, Frequency: 266, Coverage: 100.00%

Fasta names not associated with each individual primer:
Primer Name: primer_1
  seq_id_a
  seq_id_b
  seq_id_c
  seq_id_d
  ```