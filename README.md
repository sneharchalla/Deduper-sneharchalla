 #                         **Reference Based PCR Duplicate Removal Tool** 
                     
 ### Purpose: 
 Given a sam file of uniquely mapped single end reads, identify and remove all PCR duplicates (retain only a single copy of each read) using a list of UMI's while: 
 - removing erroneous UMI's 
 - accounting for all possible CIGAR strings(including adjusting for soft clipping) 
 - avoiding loading eveything into memory 
 - ensuring that the first read encountered(if duplicates are found) is the output
 - ensuring the output of a properly formatted SAM file 

### Description: 
During RNA seq library preparation, PCR is performed to add the sequencing adapters to the fragments and to amplify the fragments if the starting quantity is low. During this process, the same fragment might get amplified multiple times to produce PCR duplicates. It is important to differentiate molecular duplicates(indicating expression levels) from PCR duplicates to avoid downstream analysis issues. PCR duplication is best done after aligning to a reference genome. Adding an UMI to each fragment before the PCR step, helps to identify the PCR duplicates. Fragments with same UMI are considered PCR duplicates. The goal is to retain only one unique read. 

### Input = SAM FILE 
### Output = file containing only unique reads

### STRATEGY: 

1. Read through the SAM file
2. Correct the positions of the reads based on the CIGAR string 
3. Identify the UMI sequence from the header
4. Store the UMI sequences in a dictionary to identify duplicates 
5. If two reads have the same UMI sequence, they are considered duplicates and only the first read is retained. 


### Functions Used: 

1. get_args()fuction: to parse the command line arguments including input SAM file, UMI file and output file. 

2. pos_correction_rev() function: to take the orginal position and a CIGAR string and correct the position based on the CIGAT string. 

3. core_logic()function: to read through the input SAM file, correct the position of the reads, idenify the UMI sequences and duplicate reads based on the UMI sequences. It also writes unique reads to the output file and prints out statistics such as: 
        * number of reads with known UMI
        * number of duplicate reads 
        * number of unique reads
        * number of original reads 


 
 


    




 

