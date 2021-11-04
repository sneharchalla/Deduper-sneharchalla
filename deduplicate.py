import argparse
import gzip
import re

def get_args():
	parser = argparse.ArgumentParser(description = "A program to identify and remove PCR duplicates")
	parser.add_argument("-fh_input", help="Input SAM file", required=True)
	parser.add_argument("-fh_umi", help="UMI file name/list of all the UMI's used", required=True)
	parser.add_argument("-fh_o", help = "Output file/unique reads", required=True)
	return parser.parse_args()

args = get_args()  

# Creating a list from the umi_file:
umi_list = open(args.fh_umi).read()#.splitlines()
umi_dict = {} # key = string concatenated (pos_strand_chrom), value = UMI 
count_umi = 0 
count_unknown = 0 #unknown umi's 
reg_obj_f = re.compile (r"(\d+)S") # efficient than calling the pattern several times use\ing re.findall
reg_obj_r = re.compile (r"\d+[MDN]")


count_umi  = 0 
count_fwdstrand = 0
count_revstrand = 0
count_unknown = 0
count_dup = 0 
count_line = 0
count_notline = 0
umi_dict_count = 0
umi_dict_add = 0 
write_count = 0
count_header = 0

# FUNCTIONS:
def pos_correction_fwd (pos:int, CIGAR:str, reg_obj_f) -> int:
	'''
	Takes an int (original position) and based on CIGAR (str) corrects the position and returns another int (corrected position)
	'''
	
	if "S" in CIGAR[:-1]:     
		#print("Hello!")
		val = reg_obj_f.search(CIGAR) #reg.obj is a pattern obj that is used to search for the pattern within CIGAR
		corrected_pos = pos - int(val.group(1)) #group(1) returns the first matched pattern. In this case searching for only one pattern.
	else:
		corrected_pos = pos
	return corrected_pos

def pos_correction_rev (pos:int, CIGAR:str, reg_obj_r) -> int: 
	'''
	Takes an int (original position) and based on CIGAR (str) corrects the position and returns another int (corrected position). When it reads a position, it takes the corresponding CIGAR string and checks if it has one or more of the letters ("M", "I", "D", "N", "S"). Every letter (if present) in the CIGAR string has a value associated with it (Ex CIGAR 23S4D8I). If the letter is present, assign the value to a count variable (ex: since D is present , count_D = 4). Loop through the entire CIGAR string and generate the counts. Then add the counts and store in variable "aligned". Final corrected pos = inital pos + value from aligned. Return corrected position. 
	'''
	
	s_val = 0
	val = reg_obj_r.findall(CIGAR)
	if "S" in CIGAR: 	
		x = re.findall("\d+[A-Z]", CIGAR)
		if "S" in x[-1]:
			s_val = x[-1].split("S")[0]
		
			print(s_val)
	else:
		s_val = 0 

	aligned =0 
	for j in val:
		temp = int(re.search(r'\d+', j). group())
		if(CIGAR == '17M931781I54M1S'):
			print(j)
			print(temp,aligned)
		aligned = temp + aligned
	
	corrected_pos = int(pos) + int(aligned) + int(s_val)
	return corrected_pos

def	print_stats():
	print("Total line count:", count_line)
	print("Total header lines:", count_header)
	print("If reached end of file:", count_notline)
	print("Number of reads with known umi:", count_umi)
	print("Number of forward reads:", count_fwdstrand)
	print("Number of reverse reads:",count_revstrand)
	print("Number of reads with unknown UMI :",count_unknown)
	print("Number of duplicate reads:",count_dup) 
	print("Number of unique reads", write_count) 
	return


def core_logic():
	''' - Open the input SAM file for reading
		- Checking for chromosome #
		- Checking for starting position (correcting for soft clipping when necessary)
		- Checking for strandedness
		- Checking for UMI
		'''
	global count_umi  
	global count_fwdstrand 
	global count_revstrand 
	global count_unknown 
	global count_dup 
	global count_line 
	global count_notline 
	global umi_dict_count
	global umi_dict_add  
	global write_count 
	global count_header

	with open (args.fh_input, "r") as fh_input, open (args.fh_umi) as fh_umi, open (args.fh_o, "w") as fh_o: 
		print("STARTINGT THE CODE")
		while True: 
			line_str = fh_input.readline()
			if not line_str:
				print("End of file")
				count_notline += 1 
				break
			else:
			
				if line_str.startswith("@"):  #checking for headers and writing to output file
					fh_o.write(line_str + "\n")
					count_header +=1
					continue
				else:
					line = line_str.strip().split()
					count_line += 1
					if count_line%100000 == 0:
					   print(count_line)
					umi = line[0].split(":")[-1]
					flag = line[1]
					chrom = line[2]
					pos = int(line[3])
					#pos1 = line[3]
					CIGAR = line[5]
					corrected_pos = 0
# Pre-processing: 		
					if umi in umi_list: # in the list of known UMI's
						count_umi +=1
						#umi_dict[umi] = [] # populte umi dict with keys and empty list as values 
						if int(flag) & 16 !=16: 
							count_fwdstrand += 1
							corrected_pos = pos_correction_fwd(pos,CIGAR,reg_obj_f)
							
						else:
							count_revstrand += 1
							corrected_pos = pos_correction_rev(pos,CIGAR,reg_obj_r)
							
					else:
						count_unknown +=1	
# Checking for duplicates using the dict:
					field_info = umi + "_" + chrom + "_" + str(corrected_pos) + "_" + flag
				
					if field_info in umi_dict.keys():
							
							count_dup += 1 # maybe try to count the duplicates per chromosome		
					else: 
						
							umi_dict[field_info] = umi
							write_count += 1
							fh_o.write(line_str) # write entire read to the output file ; unique read	
							
				
	return

core_logic()
print_stats()

