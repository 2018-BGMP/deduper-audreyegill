# Deduper Part 1

Identify duplicate reads and separate input file into duped and non-duped output files. Duplicated files will have the same:   

* UMI
* Start position
* Chromosome/Contig/Etc
* Strand

Use `samtools sort` to sort the sam file by RNAME. Track RNAME of previous line for each new line; if they are the same, continue. If they are different, start a new ID set (see below for details).

Then adjust start position. Start positions are affected by soft clipping, indels, etc and should be handled differently depending on the strand. ID soft clipping with CIGAR string and strand with bitwise flag and correct position accordingly.

Once start position has been fixed, create an ID for each position, strand, and UMI combination encountered. 
The chromosome isn't necessary for this ID because we have ensured above that we are within the same chromosome. 
Check to see if the ID is in a created set of IDs. If it isn't, add it and write line to output. If it is in the set, move to the next line.

# In this directory there are...

* example input and expected output files
  * test_sam_sorted.sam
  * test_sam_output.sam
* sudo code
  * dedupe_sudo.py

