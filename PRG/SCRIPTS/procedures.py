import pandas as pd
import numpy as np
import os
import FireFiles as ff
import matplotlib.pyplot as plt
import PATHS


def fast_fourier(dfy, freq):
    fft_df = np.fft.fft(dfy)
    freqs = np.fft.fftfreq(len(dfy), d=1 / freq)

    clean_fft_df = abs(fft_df)
    clean_freqs = abs(freqs[0:len(freqs // 2)])
    return clean_fft_df[:int(len(clean_fft_df) / 2)], clean_freqs[:int(len(clean_freqs) / 2)]


def get_pauses(df, marker, std_threshold=0.02, pause_min_frame=100, limit_range=199, title=""):
    markerx = marker[:-1] + "x"
    markery = marker[:-1] + "y"
    markerz = marker[:-1] + "z"
    plt.plot(df["Frame"], df[markerx], label=markerx)
    plt.plot(df["Frame"], df[markery], label=markery)
    plt.plot(df["Frame"], df[markerz], label=markerz)
    # plt.plot(df["Frame"], df[marker], label=marker)
    xticks = [x for x in range(0, len(df["Frame"]), 100)]
    plt.xticks(xticks, rotation=80)

    len_recording = len(df[marker])
    x1 = 0
    x2 = x1 + limit_range
    pauses = []
    in_pause = False
    x1_pause = 0
    x2_pause = 0

    for x in range(len_recording - limit_range):
        region = df[marker][x:x + limit_range]
        local_std = np.std(region)

        if local_std < std_threshold and in_pause is False:
            x1_pause = x
            in_pause = True
        if local_std < std_threshold and in_pause is True:
            plt.scatter(x, local_std, color="red")
        if local_std > std_threshold and in_pause is True:
            x2_pause = x
            x1 = x2
            x2 += limit_range
            # pauses.append([x1_pause, x2_pause])
            in_pause = False
        if local_std > std_threshold and in_pause is False:
            x2 += 1
            x1 += 1
    mean = np.mean(df[marker])
    for p in xticks:
        plt.axvspan(p[0], p[1], alpha=.5, color='green')

    title = f"{title} "
    plt.title(title)
    plt.legend()
    plt.show()
    plt.close()


def get_ploted_marker(df, marker, title=""):
    markerx = marker[:-1] + "x"
    markery = marker[:-1] + "y"
    markerz = marker[:-1] + "z"
    plt.plot(df["Frame"], df[markerx], label=markerx)
    plt.plot(df["Frame"], df[markery], label=markery)
    plt.plot(df["Frame"], df[markerz], label=markerz)
    xticks = [x for x in range(0, len(df["Frame"]), 100)]
    plt.xticks(xticks, rotation=80)
    for p in xticks:
        plt.axvline(p, color="green", linewidth=0.5)

    title = f"{title} "
    plt.title(title)
    plt.legend()
    plt.show()
    plt.close()


def opti():
    opti = ff.get_all_files("DAT\\")
    opti_results = []
    for o in opti:
        if "optimization" in o:
            opti_results.append(o)

    for opti_file in opti_results:
        with open(opti_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                exercise = line.split("\t")[0].split(":")[1]
                marker = line.split("\t")[1].split(":")[1]
                limit = int(line.split("\t")[2].split(":")[1])
                std_thresh = float(line.split("\t")[3].split(":")[1])
                n_pause = int(line.split("\t")[4].split(":")[1])

                if n_pause == 9 or n_pause == 10:
                    all_files = ff.get_all_files("DAT\\")
                    tested_file = []
                    for t in all_files:
                        if exercise + ".csv" in t and exercise == "LoJu-010":
                            print(t)
                            df = pd.read_csv(t)
                            title = f"{exercise} {marker} limit{limit} std{std_thresh} "
                            get_pauses(df, marker, limit_range=limit, std_threshold=std_thresh,
                                       pause_min_frame=200, title=title)


def cut_excel_files():
    paths = ff.get_all_files(r"E:\XSENS_ANALYSIS\DAT")
    excluded_paths = []
    for p in paths:
        if ".xlsx" in p and "coupure" not in p and "Fluidite" not in p and "fluidite" not in p: # and "AnKo" not in p:  # and "001_NnPp" in p:
            excluded_paths.append(p)
    print(excluded_paths)
    for p in excluded_paths:
        print(p)
        name = os.path.basename(p).split("_")[1].split(".")[0].split("-")[0]  # DoMa
        markers = {"001": "Pelvis x", "002": "Neck z",
                   "003": "Pelvis y", "004": "L3 y",
                   "005": "Head z", "006": "Head z",
                   "007": "Head z", "008": "Right Forearm x",
                   "009": "Right Forearm y", "010": "Right Forearm z",
                   "011": "Right Forearm y"},

        identity = os.path.basename(p).split(".")[0].split("-")[0]  # 003_DoMa
        exercise = os.path.basename(p).split(".")[0].split("-")[1]  # 001
        marker = name + "-" + exercise  # DoMa-001
        # pauses = pr.get_pauses(df, markers[marker][0], title=identity)
        cut_name = identity + "_" + "coupure.xlsx"
        cut_file = ff.get_all_files(PATHS.XSENS)
        coupure_paths = []
        for c in cut_file:
            if cut_name in c:
                coupure_paths.append(c)

        cut_df = pd.read_excel(coupure_paths[0])  # stock the cuts for each exercise
        try:
            print(exercise)
            cuts = cut_df[exercise].to_list()[0].split(",")  # list of the cuts for this exercise
            cuts.insert(0, 0)
        except AttributeError:
            print("INVALID VALUES - EXERCISE IGNORED")
            continue
        sheets_to_cut = ['Segment Position', 'Segment Velocity', 'Joint Angles ZXY',
                         'Ergonomic Joint Angles ZXY', 'Ergonomic Joint Angles XZY',
                         ]

        cut_df = []  # [sheet1_cuts[[cut1], [cut2]...], sheet2_cuts[[cut1], [cut2]...]...] the whole exercise dataframe cut
        for sheet in sheets_to_cut:
            df_sheet = pd.read_excel(p, sheet_name=sheet)
            sheet_cuts = []
            current_cut = 0

            while current_cut < len(cuts):
                if current_cut == len(cuts) - 1:
                    low_cut = int(cuts[current_cut])
                    sheet_cuts.append(df_sheet.iloc[low_cut:])
                else:
                    low_cut = int(cuts[current_cut])
                    high_cut = int(cuts[current_cut + 1])
                    sheet_cuts.append(df_sheet.iloc[low_cut:high_cut])

                current_cut += 1
            cut_df.append(sheet_cuts)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            for c in range(len(cuts)):
                print(f"writing {identity}-{exercise}-repeat{c}.xlsx SHEET {sheet}")
                ff.verify_dir(rf"{PATHS.XSENS}\{identity}\repeats")
                writer = pd.ExcelWriter(
                    rf"{PATHS.XSENS}\{identity}\repeats\{exercise}-repeat{c}.xlsx",
                    engine='xlsxwriter')

                # Write each dataframe to a different worksheet.
                n = 0
                for sheet_cut in cut_df:
                    sheet_cut[c].to_excel(writer, sheet_name=sheets_to_cut[n])
                    n += 1

                # Close the Pandas Excel writer and output the Excel file.
                writer.save()
