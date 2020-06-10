import numpy as np
import matplotlib.pyplot as plt
from lofasm.bbx import bbx
import os
import sys
import glob
from lofasm import parse_data as pdat



#loco2bx.py to obtain bbx files with arrays	
def loco(n):
	cwd1 = os.getcwd()

	
	print(str(n) + " files to look at")
	j = 1
	for filename in os.listdir(cwd1):	

		print("\n Converting "+filename+" to .bbx...")	
	
		if filename.endswith(".lofasm.gz"):
			os.system("loco2bx.py -p CC,DD,CD " + filename)
			print(os.path.join(filename) +" converted to bbx ("+str(j)+"/"+str(n)+")")
			j+=1	


def numpyf(n, filei):
	
	countbinCC = np.zeros((n,1024))

	countbinDD = np.zeros((n,1024))
	
	countbinCD = np.zeros((n,1024), dtype=complex)
	
	cwd1 = os.getcwd()
	#go into CC channel and take an average of the values in the array
	os.chdir(cwd1+"/bbx/CC")
	cwd2 = os.getcwd()
	i = 0

	lst = os.listdir(cwd2)
	lst.sort()	
	for filename2 in lst:	
		if filename2.endswith(".bbx.gz"):
			lf = bbx.LofasmFile(os.path.join(filename2))
			lf.read_data()
			
			
			countbinCC[i] = np.average(lf.data, axis=0)
			print(filename2 + " avg bin added to array")	
			
			i += 1	
		
		
			lf.close()

	#go into DD channel and take an average of the values in the array
	os.chdir(cwd1)
	os.chdir(cwd1+"/bbx/DD")
	cwd3 = os.getcwd()
	i = 0

	lst = os.listdir(cwd3)
	lst.sort()	
	for filename3 in lst:	
		if filename3.endswith(".bbx.gz"):
			df = bbx.LofasmFile(os.path.join(filename3))
			df.read_data()
			
			
			countbinDD[i] = np.average(df.data, axis=0)
			print(filename3 + " avg bin added to array")	
	
			i += 1		
	
			
			
			df.close()
	
		
	#go into CD channel and take an average of the values in the array
	os.chdir(cwd1)
	os.chdir(cwd1+"/bbx/CD")
	cwd4 = os.getcwd()
	i = 0
	
	lst = os.listdir(cwd4)
	lst.sort()
	
	for filename4 in lst:	
		if filename4.endswith(".bbx.gz"):
			df = bbx.LofasmFile(os.path.join(filename4))
			df.read_data()
			
	
			countbinCD[i] = np.average(df.data, axis=0)
			print(filename4 + " avg bin added to array")	
	
			i += 1		
	
			
			
			df.close()
	
	
	#save/plot the output
	os.chdir(cwd1)
	
	filesv = filei[:-1] 
	
	np.save(str(filesv)+'outputbinCC', countbinCC)

	np.save(str(filesv)+'outputbinDD', countbinDD)
	
	np.save(str(filesv)+'outputbinCD', countbinCD)



#user input, and set up appropiate folders
mn = input('How many days would you like to process?\n')
d={}
for i in range(mn):
	x = input('Input the dates of files you are looking at. I.E.: "20190617"\n(The date will only be used as an identifier for output files)')
	d['date'+str(mn+1)] = x
	fname = str(x)
	if not os.path.exists(fname):
		os.mkdir(fname)
		print("Directory ", fname, " created")
	else:
		print("Directory ", fname, " already exists")
	

#download
for filei in glob.glob("*/20"):
	v=1
	os.chdir(filei)
	cw=os.getcwd()	
	print("Day "+str(v)+"/"+str(mn))
	os.system("rclone copy lofasm:shane/"+filei+" "+cw+" --drive-shared-with-me --progress")
	
	
	n = len(glob.glob1(cw, "*.lofasm.gz"))
	loco(n)	
	numpyf(n, filei)
	os.chdir("..")
	v+=1


