import os
import ROOT as rt  # type: ignore
import cmsstyle as CMS
import math

def create_canvas(
        canvName,   # str
        ranges,     # Dict[str, Tuple[float, float]],
        nameAxis,   # Dict[str, str],
        logAxis     = {"x": False, "y": True, "z": False},
        square      = CMS.kRectangular,
        extraSpace  = 0,
        ):
    """ Create a canvas object """

    # === put arguments in a dict

    canv_infos = {
        "canvName": canvName,
        "x_min": ranges["x"][0],
        "x_max": ranges["x"][1],
        "y_min": ranges["y"][0],
        "y_max": ranges["y"][1],
        "nameXaxis": nameAxis["x"],
        "nameYaxis": nameAxis["y"],
        "square": square,
        "extraSpace": extraSpace,
    }

    # ==== Set top right text

    # CMS.SetLumi("2016, 35.8 fb^{#minus1}", unit = None)

    # ==== Set up left text inside canvas

    CMS.SetExtraText(r"BR(t\bar{t}\rightarrowq\bar{q'}l^{\pm}\nu_{l}) = 29.2% (l = e, \mu)" )

    # ==== Create ref to upper and ratio pad

    upper_pad = None
    ratio_pad = None

    # ==== Creating the canvas

    # == If no ratio pad, only create the upper pad, set the axis
    if not "r" in ranges:
        canv = CMS.cmsCanvas(**canv_infos)
        canv.SetLogy(logAxis["y"])
        canv.SetLogx(logAxis["x"])

    # == If there is a ratio pad, create both upper and ratio pad, set the axis
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
        ref_line = rt.TLine(canv_infos["x_min"], 1, canv_infos["x_max"], 1)
        CMS.cmsDrawLine(ref_line, lcolor=rt.kBlack, lstyle=rt.kDotted, lwidth=2)
        upper_pad.cd()

    return canv, upper_pad, ratio_pad

# ===========

def create_leg(
    n_legentries,       # int
    colwidth            = 0.20,
    x_high              = 0.9,
    y_high              = 0.88,
    textSize            = 0.05,
    height_per_legitem  = 0.07,
    ):
    """ Create legend object """

    # == Set the proper number of colums

    n_legentries_per_col = 6
    n_legcols = int((n_legentries - 1) / n_legentries_per_col + 1)

    # == Set the margins

    leg_x_high = x_high
    leg_x_low = leg_x_high - n_legcols * colwidth
    leg_y_high = y_high

    max_num_entries_per_col = math.ceil(float(n_legentries) / float(n_legcols))
    leg_y_low = leg_y_high - height_per_legitem * max_num_entries_per_col

    # == Create the legend

    leg = CMS.cmsLeg(leg_x_low, leg_y_low, leg_x_high, leg_y_high, textSize=textSize)
    leg.SetNColumns(n_legcols)

    return leg

# =============

def main():

    palette = ['#5790fc', '#f89c20', '#e42536']
    root_palette = [rt.TColor.GetColor(c) for c in palette]

    # ======== I/O

    indir = "./outputs/"
    outdir = "./plots/"
    scales = ["HT_2", "HT_4", "m_ttx_2", "mT_tx"]

    for top in ["t1", "t2"]:

        top_label = {"t1": "t_{high}", "t2": "t_{low}"}[top]

        for fname in scales:

            CMS.SetLumi("2016, 35.8 fb^{#minus1}", unit = None)

            # =========== creating canvas and legend

            canv, upper_pad, ratio_pad = create_canvas(
                    canvName    = "test_canvas",
                    ranges      = {"x": (0., 800.), "y": (5.e-4, 1.e1), "r": (0.2, 1.3)},
                    logAxis     = {"x": False, "y": True}, 
                    nameAxis    = {"x": f"p_{{T, {top_label}}}", "y": rf"d\sigma/dp_{{T, {top_label}}} [pb #times GeV^{{-1}}]", "r": r"\frac{Data}{NNLO}"},
                    square      = True,
                    extraSpace  = 0.025,
                    )

            leg = create_leg( n_legentries = 4)

            # text label

            text_label = {
                    'HT_2': 'H_{T} / 2',
                    'HT_4': 'H_{T} / 4',
                    'm_ttx_2': r'm_{t\bar{t}} / 2',
                    'mT_tx': r'm_{T, \bar{t}}',
                    }[fname]

            scale_label = rt.TLatex()
            scale_label.SetNDC()
            scale_label.SetTextAngle(0)
            scale_label.SetTextColor(rt.kBlack)
            scale_label.SetTextFont(52)
            scale_label.SetTextAlign(11)
            scale_label.SetTextSize(0.06)

            scale_label.DrawLatex(0.3, 0.838, text_label)

            # ==== ratio pad

            ratio_pad.cd()
            ref_line = rt.TLine(0, 1, 800, 1)
            CMS.cmsDrawLine(ref_line, lcolor=rt.kBlack, lstyle=rt.kDotted, lwidth=2)

            # ==== Readingg and plotting Data

            infile = rt.TFile.Open(indir + fname + ".root", "read")

            # infile = rt.TFile.Open("./inputs/HEPData-ins1663958-v2-root.root", "read")

            # table_idx = {"t1": "Table 174", "t2": "Table 176"}[top]
# 
            # table = infile.Get(table_idx)
            # data_graph = table.Get("Graph1D_y1")
            # data_hist = table.Get("Hist1D_y1")
            # data_hist.SetDirectory(0)

            data_graph = infile.Get(f'{top}_data')
            data_norm = infile.Get(f'{top}_normalized_data')

            upper_pad.cd()
            CMS.cmsDraw(h = data_graph, style = "", marker = 0, mcolor = rt.kBlack, fcolor = rt.kBlack, alpha = .5)
            leg.AddEntry(data_graph, "Data", "lp")

            ratio_pad.cd()
            CMS.cmsDraw(h = data_norm, style = "", marker = 0, mcolor = rt.kBlack, fcolor = rt.kBlack, alpha = .5)


            # infile.Close()

            # =========== reading data

            # plotting kwargs
            plot_args = {
                f"plot.pT_{top}..LO": {
                    "mcolor": root_palette[0],
                    "leg_entry": "LO",
                },
                f"plot.pT_{top}..NLO.QCD": {
                    "mcolor": root_palette[1],
                    "leg_entry": "NLO",
                },
                f"plot.pT_{top}..NNLO.QCD": {
                    "mcolor": root_palette[2],
                    "leg_entry": "NNLO",
                },
            }

            # TODO: same distribution, at different orders, + data and ratio plot

            hist_list = []

            for dist in [
                f"plot.pT_{top}..LO",
                f"plot.pT_{top}..NLO.QCD",
                f"plot.pT_{top}..NNLO.QCD",
                ]:

                upper_pad.cd()

                graph = infile.Get(dist)
                # hist = infile.Get(dist + "_TH1F")
                # hist.SetDirectory(0)
                # hist_list.append(hist)

                # =========== plotting

                graph_args = {
                        "h": graph,
                        "style": "",
                        "marker": 0,
                        # "msize": 10,
                        "mcolor": plot_args[dist]["mcolor"],
                        "fcolor": plot_args[dist]["mcolor"],
                        # "fstyle": 3002,
                        "alpha": .5,
                        }
                CMS.cmsDraw(**graph_args)

                leg.AddEntry(graph, plot_args[dist]["leg_entry"], "lp")

                ratio_pad.cd()

                graph = infile.Get(dist + "_ratio")

                graph_args = {
                        "h": graph,
                        "style": "",
                        "marker": 0,
                        # "msize": 10,
                        "mcolor": plot_args[dist]["mcolor"],
                        "fcolor": plot_args[dist]["mcolor"],
                        # "fstyle": 3002,
                        "alpha": .5,
                        }

                CMS.cmsDraw(**graph_args)

            infile.Close()

            # ===== ratio pad

            # ratio_pad.cd()
            # data_ratio = data_hist.Clone()
            # LO_ratio = hist_list[0].Clone()
            # NLO_ratio = hist_list[1].Clone()
            # NNLO_hist = hist_list[2].Clone()
# 
            # data_ratio.Divide(NNLO_hist)
            # LO_ratio.Divide(NNLO_hist)
            # NLO_ratio.Divide(NNLO_hist)
# 
# 
# 
            # CMS.cmsDraw(h = data_ratio, style = "L", marker = 0, mcolor = rt.kBlack, fcolor = rt.kBlack, alpha = .5)
            # CMS.cmsDraw(h = LO_ratio, style = "L", marker = 0, mcolor = rt.kBlue, fcolor = rt.kBlue, alpha = .5)
            # CMS.cmsDraw(h = NLO_ratio, style = "L", marker = 0, mcolor = rt.kRed, fcolor = rt.kRed, alpha = .5)
# 
            # CMS.cmsDrawLine(line = data_ratio,  lcolor = rt.kBlack, lstyle=rt.kSolid)
            # CMS.cmsDrawLine(line = LO_ratio,  lcolor = rt.kBlue)
            # CMS.cmsDrawLine(line = NLO_ratio,  lcolor = rt.kRed)
 
            # ===== saving plot

            if upper_pad:
                upper_pad.cd()
                CMS.fixOverlay()
                ratio_pad.cd()
                CMS.fixOverlay()
            else:
                canv.cd()
                CMS.fixOverlay()

            # ==== size of axis labels

            # rt.gStyle.SetLabelSize(0.003, "XYZ")
            # rt.gPad.RedrawAxis()
            # CMS.FixXAxisPartition(canv, bins = [0, 40, 80, 120, 160, 200, 240, 280, 330, 380, 430, 500, 800])
            # import pdb; pdb.set_trace()


            CMS.SaveCanvas(canv, outdir+fname+"_" + top+".pdf")

if __name__ == "__main__":
    # CMS.setCMSStyle()
    # CMS.cmsStyle.SetLabelSize(0.003, "XYZ")
    main()

