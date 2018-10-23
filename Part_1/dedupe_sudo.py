# Deduper assignment
# Part 1
# Sudo


def check_bitwise(flag):
    '''Uses bitwise flag to return strand direction ('+' or '-')'''
    return strand
    
def  adjust_position(line):
    '''Return the corrected starting position of a read as a string'''
    CIGAR=line.split('\t')[6]
    if check_bitwise(line.split('\t')[3])=='+':
        
        # only adjust if first letter isn't an M
            # so position = 10 and CIGAR = 5S95M would return correct_position = '5'
        # otherwise correct_position = position
        
    elif check_bitwise(line.split('\t')[3])=='-':
    
        # different rules for different starting letters; that is...
            # position = 50	and CIGAR = 20M10S returns correct_position = '80'
            # position = 55 and CIGAR = 5S25M returns correct_position = '80'
        
    else: 
        # probably return an error just bc
        
    return 'correct position as a string'

    
    
# Sort sam file using samtools sort -o sorted_data.sam data.sam 
file = sorted_data.sam    
with open(file, 'r') as f:
    if line startswith '@':
        go to the next line
    rname_prev = ''
    ID_set = set()
    for line in f:
        
        # Ensure on same chromo/whatever
        rname = str(line.split('\t')[3])
        if rname == rname_prev:
            continue
        else:
            reset ID_set
        
        # need to change indents/nesting for the above conditionals
        # will worry about later

        
        # Use adjust_position function
        pos_corrected = adjust_position(line)
        
        # Get UMI
        UMI = line.split('\t')[1].split(':')[-1]
        # Get strand
        strand = check_bitwise(line.split('\t')[3])
        
        # create ID
        ID = rname+pos_corrected+strand+UMI
        
        if ID not in ID_set:
            add ID to ID_set
            write line to deduped.sam
        else:
            # trash the line; that is, 
            continue
        # store rname_prev
        rname_prev = rname
        
        # loop starts over, new line
        
        
        
        
    
    


    
