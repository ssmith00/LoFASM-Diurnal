import numpy as np
import matplotlib.pyplot as plt
from lofasm.bbx import bbx
import os
import sys
import glob
from lofasm import parse_data as pdat

#create an array of length equal to the number of files to be looked at
cwd1 = os.getcwd()

#n = len(glob.glob1(cwd1, "*.lofasm.gz"))

n=284

print(str(n) + " files to look at")
date = input('What is the date of the current directory? I.E.: "20190617" \n  (The date will only be used as an identifier for output files)')

countavgCC = np.zeros(n)
countfreqCC = np.zeros(n)
countbinCC = np.zeros((n,1024))

countavgDD = np.zeros(n)
countfreqDD = np.zeros(n)
countbinDD = np.zeros((n,1024))

countavgCD = np.zeros(n)
countfreqCD = np.zeros(n)
countbinCD = np.zeros((n,1024), dtype=complex)


#run loco2bx.py to obtain bbx files with arrays	

j = 1
'''
for filename in os.listdir(cwd1):	

	print("\n Converting "+filename+" to .bbx...")	
	
	if filename.endswith(".lofasm.gz"):
		os.system("loco2bx.py -p CC,DD,CD " + filename)
		print(os.path.join(filename) +" converted to bbx ("+str(j)+"/"+str(n)+")")
		j+=1	
'''
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

		countavgCC[i] = np.average(lf.data)
		print(filename2 + " average added to array")
		print("\naverage = " + str(countavgCC[i]))
		
		spect_avg = np.average(lf.data, axis=0)
		countfreqCC[i] = spect_avg[pdat.freq2bin(50)]
		print(filename2 + " freq added to array")
		print("average freq = " + str(countfreqCC[i]))
		
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

		countavgDD[i] = np.average(df.data)
		print(filename3 + " average added to array")
		print("\naverage = " + str(countavgDD[i]))
		
		spect_avg = np.average(df.data, axis=0)
		countfreqDD[i] = spect_avg[pdat.freq2bin(50)]
		print(filename3 + " freq added to array")
		print("average freq = " + str(countfreqDD[i]))
		
		countbinDD[i] = np.average(df.data, axis=0)
		print(filename3 + " avg bin added to array")	

		i += 1		

		
		
		df.close()
#*******************change to 1 to output CD files!!!***************************
runcd = 1	
	
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

		countavgCD[i] = np.average(df.data)
		print(filename4 + " average added to array")
		print("\naverage = " + str(countavgCD[i]))
		
		spect_avg = np.average(df.data, axis=0)
		countfreqCD[i] = spect_avg[pdat.freq2bin(50)]
		print(filename4 + " freq added to array")
		print("average freq = " + str(countfreqCD[i]))

		countbinCD[i] = np.average(df.data, axis=0)
		print(filename4 + " avg bin added to array")	

		i += 1		

		
		
		df.close()


#average over the individual bins

#save/plot the output
os.chdir(cwd1)

np.save(str(date)+'outputavgCC', countavgCC)
np.save(str(date)+'outputspectavgCC',countfreqCC)
np.save(str(date)+'outputbinCC', countbinCC)

np.save(str(date)+'outputavgDD', countavgDD)
np.save(str(date)+'outputspectavgDD', countfreqDD)
np.save(str(date)+'outputbinDD', countbinDD)

if runcd == 1:
	np.save(str(date)+'outputavgCD', countavgCD)
	np.save(str(date)+'outputspectavgCD', countfreqCD)
	np.save(str(date)+'outputbinCD', countbinCD)

plt.plot(countavgCC)
plt.show()
