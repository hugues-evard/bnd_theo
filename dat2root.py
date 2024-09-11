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

def normalize_data(indir, top):
    """ Convert a single distribution from a .dat file to a TGraphAssymErrors object, normalized to NNLO """

    scale_nnlo = np.genfromtxt(indir + f'plot.pT_{top}..NNLO.QCD.dat', usecols=(1))

    global BR
    scale_nnlo *= BR

    # number of bins
    nbins = len(scale_nnlo) - 1

    # ======== getting data 

    table_idx = {'t1': 'Table 174', 't2': 'Table 176'}[top]

    datafile = rt.TFile.Open('./inputs/HEPData-ins1663958-v2-root.root', 'read')
    table = datafile.Get(table_idx)
    graph = table.Get("Graph1D_y1")
    norm_graph = graph.Clone()

    graph.SetName(top + '_data')
    norm_graph.SetName(top + '_normalized_data')

    datafile.Close()

    # ======== Normalizing

    for i in range(nbins-1):
        norm_graph.SetPointY(i, graph.GetPointY(i) / scale_nnlo[i])
        norm_graph.SetPointEYlow(i, graph.GetErrorYlow(i) / scale_nnlo[i])
        norm_graph.SetPointEYhigh(i, graph.GetErrorYhigh(i) / scale_nnlo[i])

    return graph, norm_graph


# ===========

def dir_to_root(indir, outpath, varlist):
    """ Convert a list of distribution in a given directory to a single .root output """

    # ==== Create a single output file for the whole directory
    data_graph_t1, data_ratio_graph_t1 = normalize_data(indir, 't1')
    data_graph_t2, data_ratio_graph_t2 = normalize_data(indir, 't2')

    outfile = rt.TFile.Open(outpath, "recreate")

    # ==== read, convert and write each distribution to a graph
    for var in varlist:
        graph = dat_to_graph(indir + var + ".dat", var)
        graph.Write()

        ratio_graph = dat_to_ratio(indir + var + ".dat", var)
        ratio_graph.Write()

    # ==== add normalized data
    
    data_graph_t1.Write()
    data_ratio_graph_t1.Write()

    data_graph_t2.Write()
    data_ratio_graph_t2.Write()

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

