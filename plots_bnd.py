import os
import ROOT as rt  # type: ignore
import cmsstyle as CMS
import math

def main():

    # ======== I/O

    indir = "./outputs/"
    outdir = "./plots/"
    # fname = "pT_thigh__NLO_QCD" 
    scales = ["HT2", "mttbar2"]

    for fname in scales:

        # =========== creating plotter and canvas

        CMS.SetLumi("Simulation, 13 TeV")

            # canvName: str,
            # ranges: Dict[str, Tuple[float, float]],
            # nameAxis: Dict[str, str],
            # logAxis: Dict[str, bool] = {"x": False, "y": True, "z": False},
            # square: bool = CMS.kRectangular,
            # iPos: int = 11,
            # extraSpace: float = 0,
            # with_z_axis: bool = False,

        upper_pad = None
        ratio_pad = None

        ranges = {"x": (0., 800.), "y": (1., 15000.)}#, "r": (-1., 1.)},
        logAxis = {"x": False, "y": True}
        nameAxis = {"x": "p_{T, t_{high}}", "y": r"d\sigma/dp_{T, t_{high}} [pb #times GeV^{-1}]"}# "r": "ratio axis"},

        canv_infos = {
            "canvName": "test_canvas",
            "x_min": ranges["x"][0],
            "x_max": ranges["x"][1],
            "y_min": ranges["y"][0],
            "y_max": ranges["y"][1],
            "nameXaxis": nameAxis["x"],
            "nameYaxis": nameAxis["y"],
            "square": True,
            "iPos": 10,
            "extraSpace": 0.075,
            # "scaleLumi": scaleLumi,
        }

        if not "r" in ranges:
            canv = CMS.cmsCanvas(**canv_infos)
            canv.SetLogy(logAxis["y"])
            canv.SetLogx(logAxis["x"])
        else:
            canv_infos["r_min"] = ranges["r"][0]
            canv_infos["r_max"] = ranges["r"][1]
            canv_infos["nameRatio"] = nameAxis["r"]
            canv = CMS.cmsDiCanvas(**canv_infos)
            upper_pad = canv.cd(1)
            ratio_pad = canv.cd(2)
            upper_pad.SetLogy(logAxis["y"])
            upper_pad.SetLogx(logAxis["x"])
            ratio_pad.cd()
            ref_line = ROOT.TLine(canv_infos["x_min"], 1, canv_infos["x_max"], 1)
            CMS.cmsDrawLine(ref_line, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted, lwidth=2)
            upper_pad.cd()

        # ===== Legend

        colwidth=0.20
        x_high=0.9
        y_high=0.88
        textSize=0.05
        height_per_legitem=0.07

        n_legentries = 2
        n_legentries_per_col = 6
        n_legcols = int((n_legentries - 1) / n_legentries_per_col + 1)
        leg_x_high = x_high
        leg_x_low = leg_x_high - n_legcols * colwidth
        leg_y_high = y_high
        max_num_entries_per_col = math.ceil(float(n_legentries) / float(n_legcols))
        leg_y_low = leg_y_high - height_per_legitem * max_num_entries_per_col
        leg = CMS.cmsLeg(leg_x_low, leg_y_low, leg_x_high, leg_y_high, textSize=textSize)
        leg.SetNColumns(n_legcols)

        # =========== reading data

        infile = rt.TFile.Open(indir + fname + ".root", "read")
        for dist in ["pT_thigh__NLO_QCD" , "pT_tlow__NLO_QCD"]:

            graph = infile.Get(dist)

            # =========== plotting

            graph_args = {
                    "h": graph,
                    "style": "P",
                    "marker": 0,
                    # "msize": 1.0,
                    "mcolor": rt.kBlack,
                    # "lstyle": rt.kSolid,
                    # "lwidth": 1,
                    # "lcolor": rt.kRed + 1,
                    # "fstyle": 1001,
                    # "fcolor": rt.kYellow + 1,
                    # "alpha": -1
                    }
            CMS.cmsDraw(**graph_args)
            leg.AddEntry(graph, "entry", "lp")

        # ===== saving plot

        if upper_pad:
            upper_pad.cd()
            CMS.fixOverlay()
            ratio_pad.cd()
            CMS.fixOverlay()
        else:
            canv.cd()
            CMS.fixOverlay()

        CMS.SaveCanvas(canv, outdir+fname+".pdf")


if __name__ == "__main__":
    main()

