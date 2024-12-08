import csv, numpy as np

with open("openings.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")
    #for line in tsv_file:
        #print(line[1], " ", line[2])



import csv, numpy as np

if __name__ == '__main__':
    with open("openings.tsv") as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            print(line[1], " ", line[2])