####################################################
#                                                  #
# B10H4CK1NG Project Series - BlastSeqFreqAnalyzer #
#                                                  #
#             Author: Aaron G. S. (Cipher)         #
#                                                  #
#              Date: 18/02/23                      #
#                                                  #
####################################################
#                                                  #
# This script reads a BLAST results file and       #
# extracts the query sequence, subject sequence,   #
# start and end positions, and frequency of        #
# occurrences for each query-subject sequence pair #                                                   #
#                                                  #
####################################################

# variable names
btable_path = "" # Path to BLAST output
output_name = "" # Output file name

# Open the BLAST results file
with open(btable_path) as f:
    lines = f.readlines()

# Create a dictionary to store the frequency and positions of the sequences
sequence_dict = {}

# Loop through each line in the BLAST results file
for line in lines:
    # Split the line into columns
    columns = line.strip().split("\t")

    # Get the query sequence and subject sequence from the columns
    query_sequence = columns[0]
    subject_sequence = columns[1]

    # Get the start and end positions from the columns
    start_position = int(columns[8])
    end_position = int(columns[9])

    # Check if the query sequence is already in the dictionary
    if query_sequence not in sequence_dict:
        # If not, add it to the dictionary with the current subject sequence and its frequency as 1
        sequence_dict[query_sequence] = {subject_sequence: {"frequency": 1, "positions": [(start_position, end_position)]}}
    else:
        # If the query sequence is already in the dictionary, check if the current subject sequence is also in the dictionary
        if subject_sequence not in sequence_dict[query_sequence]:
            # If not, add it to the dictionary with the frequency as 1
            sequence_dict[query_sequence][subject_sequence] = {"frequency": 1, "positions": [(start_position, end_position)]}
        else:
            # If the subject sequence is already in the dictionary, increase its frequency by 1
            sequence_dict[query_sequence][subject_sequence]["frequency"] += 1
            sequence_dict[query_sequence][subject_sequence]["positions"].append((start_position, end_position))

# Open a new file to write the results
with open(output_name, "w") as f:
    # Write the header line to the file
    f.write("Query Sequence;Subject Sequence;Frequency;Positions\n")

    # Loop through the dictionary and write the results to the file
    for query_sequence, subject_sequences in sequence_dict.items():
        for subject_sequence, data in subject_sequences.items():
            positions_str = ",".join([f"{start}-{end}" for start, end in data["positions"]])
            f.write(f"{query_sequence};{subject_sequence};{data['frequency']};{positions_str}\n")
