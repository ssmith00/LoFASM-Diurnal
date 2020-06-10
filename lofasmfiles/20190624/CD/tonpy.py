import os
import numpy as np
from lofasm.bbx import bbx

cwd = os.getcwd()

for filei in os.listdir(cwd):
	if filei.endswith(".bbx.gz"):
		lf = bbx.LofasmFile(os.path.join(filei))
		lf.read_data()
		
		np.save(filei, lf.data)
		lf.close()	
