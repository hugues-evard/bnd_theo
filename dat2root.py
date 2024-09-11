import ROOT as rt
from array import array
import numpy as np

# ===========
BR = 0.438 * 2./3.
# 43.8% for semileptonic, 2/3 for only e and μ, not τ

def dat_to_graph(infile, graph_name):
    """ Convert a single distribution from a .dat file to a TGraphAssymErrors object """

    arr = np.genfromtxt(infile, usecols=(0,1,2,3,4,5))

    # number of bins
    nbins = len(arr) - 1

    # binning
    bin_low = arr[:-1,0]
    bin_high = arr[1:,0]
    bin_center = (bin_high + bin_low) / 2

    edges = array('d', arr[:, 0])

    # scale value
    scale_center = arr[:, 1]
    scale_low = arr[:, 3]
    scale_high = arr[:, 5]

    # multiplying scale by BR
    global BR
    scale_center *= BR
    scale_low *= BR
    scale_high *= BR

    # ======== converting to TGraphAsymmErrors

    graph = rt.TGraphAsymmErrors()
    graph.SetName(graph_name)
    graph.Set(nbins-1)

    # == filling the graph
    for i in range(nbins-1):
        graph.SetPoint(i, bin_center[i], scale_center[i])
        graph.SetPointError(i, bin_center[i] - bin_low[i], bin_high[i] - bin_center[i],
            scale_center[i] - scale_low[i], scale_high[i] - scale_center[i],
            )

    return graph

def dat_to_ratio(infile, graph_name):
    """ Convert a single distribution from a .dat file to a TGraphAssymErrors object, normalized to NNLO """

    arr = np.genfromtxt(infile, usecols=(0,1,2,3,4,5))

    # number of bins
    nbins = len(arr) - 1

    # binning
    bin_low = arr[:-1,0]
    bin_high = arr[1:,0]
    bin_center = (bin_high + bin_low) / 2

    edges = array('d', arr[:, 0])

    # scale value
    scale_center = arr[:, 1]
    scale_low = arr[:, 3]
    scale_high = arr[:, 5]

    # multiplying scale by BR
    # global BR
    # scale_center *= BR
    # scale_low *= BR
    # scale_high *= BR

    # ======== Normalizing

    den_arr = np.genfromtxt('..'.join(infile.split('..')[:-1] + ['NNLO.QCD.dat']), usecols = (1))

    scale_center /= den_arr
    scale_low /= den_arr
    scale_high /= den_arr

    # ======== converting to TGraphAsymmErrors

    graph = rt.TGraphAsymmErrors()
    graph.SetName(graph_name + "_ratio")
    graph.Set(nbins-1)

    # == filling the graph
    for i in range(nbins-1):
        graph.SetPoint(i, bin_center[i], scale_center[i])
        graph.SetPointError(i, bin_center[i] - bin_low[i], bin_high[i] - bin_center[i],
            scale_center[i] - scale_low[i], scale_high[i] - scale_center[i],
            )

    return graph

def dat_to_TH1F(infile, hist_name):
    """ Convert a single distribution from a .dat file to a TGraphAssymErrors object """

    arr = np.genfromtxt(infile, usecols=(0,1,2,3,4,5))

    # number of bins
    nbins = len(arr) - 1

    # binning
    bin_low = arr[:-1,0]
    bin_high = arr[1:,0]
    bin_center = (bin_high + bin_low) / 2

    edges = array('d', arr[:, 0])

    # scale value
    scale_center = arr[:, 1]
    scale_low = arr[:, 3]
    scale_high = arr[:, 5]

    # Multiplying scale by BR:
    global BR
    scale_center *= BR
    scale_low *= BR
    scale_high *= BR

    # ======== converting to TH1F

    hist = rt.TH1F(hist_name + "_TH1F", hist_name + "_TH1F", nbins - 1, array('d', list(bin_low)))

    # == filling the hist
    for i in range(nbins- 1):
        hist.SetBinContent(i+1, scale_center[i])

    return hist

# ===========

def dir_to_root(indir, outpath, varlist):
    """ Convert a list of distribution in a given directory to a single .root output """

    # ==== Create a single output file for the whole directory
    outfile = rt.TFile.Open(outpath, "recreate")

    # ==== read, convert and write each distribution to a graph
    for var in varlist:
        graph = dat_to_graph(indir + var + ".dat", var)
        graph.Write()

        ratio_graph = dat_to_ratio(indir + var + ".dat", var)
        ratio_graph.Write()

        hist = dat_to_TH1F(indir + var + ".dat", var)
        hist.Write()

    # ==== close the output file
    outfile.Close()

# ===========
    

if __name__ == "__main__":
    
    outdir = "./outputs/"
    varlist = [
        "plot.pT_t1..LO",
        "plot.pT_t1..NLO.QCD",
        "plot.pT_t1..NNLO.QCD",
        "plot.pT_t2..LO",
        "plot.pT_t2..NLO.QCD",
        "plot.pT_t2..NNLO.QCD",
        ]

    for scale in ["HT_2", "HT_4", "m_ttx_2", "mT_tx"]:

        indir = f"./inputs/{scale}/"
        dir_to_root(indir, outdir + scale + ".root", varlist)

