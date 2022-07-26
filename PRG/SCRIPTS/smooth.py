import pandas as pd
import numpy as np
import os
import FireFiles as ff
from PRG.SPARC_master.scripts.smoothness import sparc
import PATHS


def smoothness():
    paths = ff.get_all_files(PATHS.XSENS)
    excluded_paths = []
    exercises = ["001", "004", "007", "010"]

    for p in paths:
        if ".xlsx" in p and "Fluidite" not in p and "coupure" not in p and not "fluidite_repeat" in p:  # and "DoMa" in p:
            if os.path.basename(p).split(".")[0].split("-")[1] in exercises:
                excluded_paths.append(p)
    for p in excluded_paths:
        name = p.split("\\")[-1].split("_")[1].split(".")[0].split("-")[0]  # DoMa

        identity = os.path.basename(p).split(".")[0].split("-")[0]  # 003_DoMa
        exercise = os.path.basename(p).split(".")[0].split("-")[1]  # 001
        marker = name + "-" + exercise  # DoMa-001

        cut_name = identity + "-" + exercise + "_" + "Fluidite"

        cut_file = ff.get_all_files(PATHS.XSENS)
        coupure_paths = []
        for c in cut_file:
            if cut_name in c:
                coupure_paths.append(c)
        for coupure in coupure_paths:
            fluid_identity = os.path.basename(coupure).split("_")[2]
            number_fluidite = ""
            if "1" in fluid_identity:
                number_fluidite = "_go"
            elif "2" in fluid_identity:
                number_fluidite = "_back"
            cut_df = pd.read_excel(coupure)  # stock the cuts for each exercise
            cuts = cut_df.columns.to_list()[0].split(",")
            if cuts[-1] == '':
                cuts.pop()

            sheets_to_cut = ['Segment Velocity', ]

            cut_df = []  # [sheet1_cuts[[cut1], [cut2]...], sheet2_cuts[[cut1], [cut2]...]...] the whole exercise dataframe cut
            for sheet in sheets_to_cut:
                df_sheet = pd.read_excel(p, sheet_name=sheet)
                sheet_cuts = []
                current_cut = 0

                while current_cut < len(cuts) - 1:
                    low_cut = int(cuts[current_cut])
                    high_cut = int(cuts[current_cut + 1])
                    sheet_cuts.append(df_sheet.iloc[low_cut:high_cut])
                    current_cut += 1
                cut_df.append(sheet_cuts)

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                for c in range(len(cuts) - 1):
                    print(f"writing {identity}-{exercise}-repeat{c}.xlsx SHEET {sheet}")
                    new_path = rf'{PATHS.XSENS}\{identity}\fluidite_repeats'
                    ff.verify_dir(new_path)
                    writer = pd.ExcelWriter(new_path + rf"\{exercise}-fluidite_repeat{c}{number_fluidite}.xlsx",
                                            engine='xlsxwriter')

                    # Write each dataframe to a different worksheet.
                    n = 0
                    for sheet_cut in cut_df:
                        sheet_cut[c].to_excel(writer, sheet_name=sheets_to_cut[n])
                        n += 1

                    # Close the Pandas Excel writer and output the Excel file.
                    writer.save()


def analysis():
    identities_results = {"003_DoMa": ([], [], [],), "002_BaEl": ([], [], [],), "004_LoJu": ([], [], [],), "005_LuWi": ([], [], [],),
                          "006_ReCo": ([], [], [],), "007_AmVi": ([], [], [],), "008_GuEm": ([], [], [],), "009_ChCl": ([], [], [],),
                          "010_AnKo": ([], [], [],), "011_YaJu": ([], [], [],), "012_PaMa": ([], [], [],), "013_SaCl": ([], [], [],),
                          "014_MoLu": ([], [], [],), "015_LaJu": ([], [], [],), "016_LaCh": ([], [], [],), "017_GoMa": ([], [], [],),
                          "018_FaFr": ([], [], [],), "019_GuAl": ([], [], [],), "020_PlSi": ([], [], [],), "021_GuGi": ([], [], [],),
                          "022_DrGe": ([], [], [],), }
    paths = ff.get_all_files(PATHS.XSENS)
    excluded_paths = []
    doubled_exercise = ["007", "010"]
    exercises = ["001", "004", "007", "010"]
    markers = {"001": ["T8 z", "Right Hand z"], "004": ["T8 z", "Pelvis z"], "007": ["T8 z", "Right Hand z"],
               "010": ["Right Hand x", "T8 x"], }
    for p in paths:
        if ".xlsx" in p and "fluidite_repeat" in p:
            excluded_paths.append(p)

    for ex in exercises:
        all_results = []
        if ex not in doubled_exercise:
            for identity in identities_results:
                ex_repeats = []

                for excluded in excluded_paths:
                    if ex in excluded:
                        ex_repeats.append(excluded)

                for marker in markers[ex]:
                    all_repeats = []
                    fluidites = []
                    for repeat in ex_repeats:
                        if identity in repeat:
                            df = pd.read_excel(repeat)
                            all_repeats.append(df[marker])

                    arrays = [np.array(x) for x in all_repeats]
                    mean_signal = [np.mean(k) for k in zip(*arrays)]
                    std_signal = [np.std(k) for k in zip(*arrays)]

                    new_sal = 0
                    try:
                        new_sal = sparc(mean_signal, 60)[0]
                    except:
                        new_sal = 0
                    identities_results[identity][0].append(round(new_sal, 3))
                    all_results.append((identity, "none", marker, new_sal))

        else:
            for identity in identities_results:
                for b_g in ["_back", "_go"]:
                    ex_repeats = []
                    for excluded in excluded_paths:
                        if ex in excluded and b_g in excluded:
                            ex_repeats.append(excluded)

                    for marker in markers[ex]:
                        all_repeats = []
                        fluidites = []
                        for repeat in ex_repeats:
                            if identity in repeat:
                                df = pd.read_excel(repeat)
                                df = df.dropna(axis=0)
                                all_repeats.append(df[marker].to_list())
                        arrays = [np.array(x) for x in all_repeats]
                        mean_signal = [np.mean(k) for k in zip(*arrays)]
                        std_signal = [np.std(k) for k in zip(*arrays)]

                        new_sal = 0
                        try:
                            new_sal = sparc(mean_signal, 60)[0]
                        except:
                            new_sal = 0
                        identities_results[identity][0].append(round(new_sal, 3))
                        identities_results[identity][1].append(b_g[1:])
                        identities_results[identity][2].append(marker)
                        #all_results.append((identity, b_g[1:], marker, new_sal))

        print(identities_results)
        with open(rf"{PATHS.RES}\smoothness_{ex}.csv", "w+") as f:
            lines = []
            lines.insert(0, "identity,smoothness,orientation,marker\n")

            for id in identities_results:
                lines.append(f"{id},{identities_results[id][0]},{identities_results[id][1]},{identities_results[id][2]}\n")
            for line in lines:
                f.write(line)
