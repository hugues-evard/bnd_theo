import ROOT as rt
from array import array
import numpy as np

# ===========

def dat_to_graph(infile, graph_name):
    """ Convert a single distribution from a .dat file to a TGraphAssymErrors object """

    arr = np.genfromtxt(infile, usecols=(0,1,2,3,4,5,6,7))

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
    graph.SetName(graph_name)
    graph.Set(nbins)

    # == filling the graph
    for i in range(nbins):
        graph.SetPoint(i, bin_center[i], scale_center[i])
        graph.SetPointError(i, bin_center[i] - bin_low[i], bin_high[i] - bin_center[i],
            scale_center[i] - scale_low[i], scale_high[i] - scale_center[i],
            )

    return graph

# ===========

def dir_to_root(indir, outpath, varlist):
    """ Convert a list of distribution in a given directory to a single .root output """

    # ==== Create a single output file for the whole directory
    outfile = rt.TFile.Open(outpath, "recreate")

    # ==== read, convert and write each distribution to a graph
    for var in varlist:
        graph = dat_to_graph(indir + var + ".dat", var)
        graph.Write()

    # ==== close the output file
    outfile.Close()


# ===========
    

if __name__ == "__main__":
    
    outdir = "./outputs/"
    varlist = ["pT_thigh__NLO_QCD" , "pT_tlow__NLO_QCD"]

    for scale in ["HT2", "mttbar2"]:

        indir = f"./inputs/run_{scale}/NLO-run/distributions__NLO_QCD/"
        dir_to_root(indir, outdir + scale + ".root", varlist)

