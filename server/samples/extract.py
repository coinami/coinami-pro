import sys
import random

if len(sys.argv) < 4:
	print "Usage: python extract.py file_name output_name n_lines [decoy|job]"
	exit(0)

decoy = False
if sys.argv[4] == "decoy":
	decoy = True

file_name = sys.argv[1]
output_name = sys.argv[2]
n_lines = int(sys.argv[3])

f = open(file_name+".1.fq")
f2 = open(file_name+".2.fq")
o = open(output_name+".1.fq","w")
o2 = open(output_name+".2.fq","w")

count = 0

while count < n_lines:
	p = []
	p2 = []
	for i in range(0,4):
		p.append(f.readline())
	for i in range(0,4):
		p2.append(f2.readline())
	if len(p[1]) == 0:
		f = open(file_name+".1.fq")
		f2 = open(file_name+".2.fq")
		continue
	if random.random() < 0.01:
		if ("N" not in p[1] and "N" not in p2[1] and decoy == True) or decoy == False:
			o.writelines(p)
			o2.writelines(p2)
			count += 1

o.close()
o2.close()
f.close()
f2.close()
