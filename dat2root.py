import ROOT as rt
from array import array
import numpy as np

# ======= I/O

indir = "./inputs/run_HT2/NLO-run/distributions__NLO_QCD/"
outdir = "./outputs/"
infile = "pT_thigh__NLO_QCD" 

# ======= reading file

arr = np.genfromtxt(indir+infile+".dat", usecols=(0,1,2,3,4,5,6,7))

# number of bins
nbins = len(arr)

# binning
bin_low = arr[:,0]
bin_high = arr[:,1]
bin_center = (bin_high + bin_low) / 2

edges = array('d', list(bin_low) + [bin_high[-1]])

# scale value
scale_center = arr[:, 2]
scale_low = arr[:, 4]
scale_high = arr[:, 6]

# ======== converting to TGraphAsymmErrors

graph = rt.TGraphAsymmErrors()
graph.SetName(infile)
graph.Set(nbins)

# == filling the graph
for i in range(nbins):
    graph.SetPoint(i, bin_center[i], scale_center[i])
    graph.SetPointError(i, bin_center[i] - bin_low[i], bin_high[i] - bin_center[i],
            scale_center[i] - scale_low[i], scale_high[i] - scale_center[i],
            )

# ======== Saving file

outfile = rt.TFile.Open(outdir+infile+".root", "recreate")
graph.Write()
outfile.Close()


