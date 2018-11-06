#!/usr/bin/env python

######################
###                ###
###    Modules     ###
###                ###
######################

import argparse
import re
import sys


########################
###                  ###
###    Arguments     ###
###                  ###
########################

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="Path to input SAM file. This should be the output from samtools sort.", type=str, required=True)
    parser.add_argument("-o","--out", help="Name of output SAM file. Defaults to <input file name>_deduped.sam", type=str, required=False)
    parser.add_argument("-u","--UMI_file", help="Path to a text file consisting only of UMIs which are separated by a new line.", type=str, required=False)
    parser.add_argument("-p", "--paired", help="Path to paired file.", required=False, type=str)
    parser.add_argument("-b", "--barcode_length", help="An integer which indicates barcode length. Defaults to 8.", type=int, required=False, default=8)
    return parser.parse_args()

args = arguments()
file = args.file
UMIs = args.UMI_file
paired = args.paired
b = args.barcode_length

if args.out is None:
    out = file.split('/')[-1]+'_deduped.sam'
else:
    out = args.out


############################
###                      ###
###    Error messages    ###
###                      ###
############################

if UMIs is None:
    sys.exit("Randomers are not supported as of Nov. 5, 2018.")
if paired is not None:
    sys.exit("Paired-end reads are not supported as of Nov. 5, 2018.")

    
#######################
###                 ###
###    Functions    ###
###                 ###
#######################    
    
def check_bitwise(flag):
    '''Uses bitwise flag to return strand direction ('+' or '-')'''
    if ((int(flag) & 16) != 16):
        strand = '+'
    else:
        strand = '-'
    return strand
    
def  adjust_position(line):
    '''Return the 5' corrected starting position of a read as a string'''
    
    # Get useful info
    CIGAR=line.split('\t')[5]
    pos = int(line.split('\t')[3])
    flag = line.split('\t')[1]
    
    # Forward Strand
    if ((int(flag) & 16) != 16):
                
        first = re.findall(r'^(\d+)([MIDNSHPX=])', CIGAR)[0]
        if first[1] == 'M':
            pos_adj = pos
        if first[1] == 'S':
            pos_adj = pos - int(first[0])
    
    # Reverse Strand
    else:
        
        last = re.findall(r'(\d+)([MIDNSHPX=])$', CIGAR)[0]
        if last[1] == 'M':
            pos_adj = pos + sum([int(i) for i in re.findall(r'(\d+)[MND]', CIGAR)]) - 1
        if last[1] == 'S':
            pos_adj = pos + sum([int(i) for i in re.findall(r'(\d+)[MND]', CIGAR)]) + int(last[0]) -1
        
    return str(pos_adj)

    
def get_UMI(line):
    '''Return the UMI in a sam file line using a predetermined barcode length b'''
    UMI = re.findall(r'([ACGTN]{%s})' % b, line)[0]
    return UMI
    

##########################
###                    ###
###      Valid UMIs    ###
###                    ###
##########################
    

valid_UMIs = set()
with open(UMIs, 'r') as umi:
    for line in umi:
        umi=get_UMI(line)
        valid_UMIs.add(umi)

        
######################
###                ###
###    Counters    ###
###                ###
######################

number_reads = 0
number_dupes = 0
number_bad_UMI = 0

####################################
###                              ###
###    Write Out Unique Reads    ###
###                              ###
#################################### 

with open(file, 'rt') as f, open(out, 'wt') as o:
    rname_prev = ''
    ID_set = set()
    for line in f:

    # This writes out then ignores headers
        if line.startswith('@'):
            o.write(line)
            continue
        
        # Once all headers are ignored...
        
        number_reads += 1
        
        # Get rname
        rname = str(line.split('\t')[2])
        
        # Reset ID_set 
        if rname != rname_prev:
            ID_set = set()
        
        # Set UMI
        UMI = get_UMI(line)
        
        # Check valid UMI
        if UMI not in valid_UMIs:
            number_bad_UMI += 1
            continue        
        
        # Get corrected position
        pos_adj = adjust_position(line)
        
        # Get strand
        strand = check_bitwise(line.split('\t')[1])
        
        # create ID
        ID = rname+'_'+pos_adj+'_'+strand+UMI
       
        if ID not in ID_set:
            ID_set.add(ID)
            o.write(line)
        else:
            # trash the line 
            number_dupes += 1
        
        # store rname_prev
        rname_prev = rname
        

##############################
###                        ###
###    Print Statements    ###
###                        ###
##############################        
        
print("Total reads: "+str(number_reads))
print("Duplicate reads: "+str(number_dupes))
print("Percent duplicates: "+str(number_dupes/number_reads))
print("Bad UMIs : "+str(number_bad_UMI))