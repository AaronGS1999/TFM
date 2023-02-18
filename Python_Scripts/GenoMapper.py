####################################################
#                                                  #
#     B10H4CK1NG Project Series - GenoMapper       #
#                                                  #
#             Author: Aaron G. S. (Cipher)         #
#                                                  #
#              Date: 18/02/23                      #
#                                                  #
####################################################
#                                                  #
#  Program to represent sequences on chromosomes   #
#       according to their position on them        #
#                                                  #
####################################################


import pandas as pd
import matplotlib.pyplot as plt

# variable names
csv_path = "tabla_helitron.csv" # path to .csv file
chr_id = "Chr_letter" # column name with the id of the chromosomes
chr_length = "chr_length" # column name with chromosome length
seq_id = "Query_Sequence" # column name with the id of the sequences
seq_p = "Positions" # column name with the positions of sequences on crhomosomes
png_name = "helitron_cromosomas_v3.png" # name of the png output

# Load the CSV file into a Pandas DataFrame
data = pd.read_csv(csv_path)

# Create a dictionary to store the color of each sequence
seq_colors = {}
color_idx = 0

# Create a dictionary to store the name of each sequence
seq_names = {}

# Create a dictionary to store the posición of each chromosome on the X axis
chromosome_positions = {}
x = 0
for chrom in data[chr_id].unique():
    chromosome_positions[chrom] = x
    x += 1

# Configure the matplotlib figure
fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

# Iterate over each chromosome in the DataFrame
for chrom, group in data.groupby(chr_id):
    # Calculate the height of the bar corresponding to the chromosome
    height = group[chr_length].iloc[0] / 1000000
    # Draw the chromosome bar
    ax.bar(chromosome_positions[chrom], height, bottom=0, align="center", alpha=0.8, color="black", width=0.8)
    # Iterate over each sequence on chromosome
    for i, row in group.iterrows():
        seq = row[seq_id]
        if seq not in seq_colors:
            seq_colors[seq] = f"C{color_idx}"
            seq_names[seq] = row[seq_id]
            color_idx += 1
        # Get the positions of the sequence
        positions = row[seq_p].split(";")
        for pos in positions:
            # Split the positions into start and end
            start, end = pos.split("-")
            start = int(start)
            end = int(end)
            # Calculate the width and center of the rectangle
            width = 0.75
            center = chromosome_positions[chrom]
            # Draw a rectangle at the corresponding position with the color of the sequence
            ax.add_patch(plt.Rectangle((float(center) - 0.375, start / 1000000), float(width), (end - start) / 1000000, color=seq_colors[seq]))

# Create the legend
legend_patches = [plt.Rectangle((0,0),1,1, color=seq_colors[seq]) for seq in seq_colors]
ax.legend(legend_patches, [seq_names[seq] for seq in seq_colors], loc="center left", bbox_to_anchor=(1, 0.5))

# Configure the X-axis labels
ax.set_xticks(list(chromosome_positions.values()))
ax.set_xticklabels(list(chromosome_positions.keys()))

# Configure the Y-axis labels
ax.set_ylabel("Tamaño del cromosoma (Mb)")

# Save and show the plot
fig.savefig(png_name, bbox_inches="tight")
plt.show()
