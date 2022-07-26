import os

import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis():
    """
    Get mean, median, and std duration while 'timed up and go' test.
    """
    # Getting al the repeats for the exercise 004
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = "004"
    sheet = "Segment Position"
    markers = ["Pelvis x", ]  # add your marker
    all_repeats = []
    for p in all_paths:
        if exercise + "-repeat" in p:
            all_repeats.append(p)

    # Getting the different participating people
    identities = []
    for r in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(r)))
        already_exist = False
        for id in identities:
            if identity in id:
                already_exist=True
        if not already_exist:
            identities.append(identity)

    # Defining and getting the metrics for all the repeats
    repeat_length = []  # add a list containing your metric for all the repeats

    identities_results = {"003_DoMa": ([],), "002_BaEl": ([],), "004_LoJu": ([],), "005_LuWi": ([],),
                          "006_ReCo": ([],), "007_AmVi": ([],), "008_GuEm": ([],), "009_ChCl": ([],),
                          "010_AnKo": ([],), "011_YaJu": ([],), "012_PaMa": ([],), "013_SaCl": ([],),
                          "014_MoLu": ([],), "015_LaJu": ([],), "016_LaCh": ([],), "017_GoMa": ([],),
                          "018_FaFr": ([],), "019_GuAl": ([],), "020_PlSi": ([],), "021_GuGi": ([],),
                          "022_DrGe": ([],), }

    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p)))
        df = pd.read_excel(p, sheet_name=sheet)

        identities_results[identity][0].append(round(max(df[markers[0]]), 3))

    # Sum up and writing file
    title = rf"{PATHS.RES}\time_004.csv"
    columns = "identity,mean duration,median duration,std duration\n"  # if new metric, add the column here

    with open(title, "w+") as f:
        lines = []
        lines.insert(0, columns)
        for id in identities_results:
            mean_duration = np.mean(identities_results[id][0])
            std_duration = np.std(identities_results[id][0])
            median_duration = np.median(identities_results[id][0])  # add your metric here (based on all repeats)

            new_line = f"{id},{round(mean_duration, 3)},{round(median_duration, 3)},{round(std_duration, 3)}\n"  # add the metric in new_line
            lines.append(new_line)
        for line in lines:
            f.write(line)

