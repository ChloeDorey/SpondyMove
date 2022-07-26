import os

import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis():
    """
    Get mean velocity, median , and std for the pelvis while walking on 10m.
    """
    # Getting al the repeats for the exercise 009
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = "009"
    sheet = "Segment Velocity"
    markers = ["Pelvis x", ]  # add your markers here
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
                already_exist = True
        if not already_exist:
            identities.append(identity)

    identities_results = {"003_DoMa": ([],), "002_BaEl": ([],), "004_LoJu": ([],), "005_LuWi": ([],),
                          "006_ReCo": ([],), "007_AmVi": ([],), "008_GuEm": ([],), "009_ChCl": ([],),
                          "010_AnKo": ([],), "011_YaJu": ([],), "012_PaMa": ([],), "013_SaCl": ([],),
                          "014_MoLu": ([],), "015_LaJu": ([],), "016_LaCh": ([],), "017_GoMa": ([],),
                          "018_FaFr": ([],), "019_GuAl": ([],), "020_PlSi": ([],), "021_GuGi": ([],),
                          "022_DrGe": ([],), }

    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p)))  # ajouter cette ligne
        df = pd.read_excel(p, sheet_name=sheet)

        identities_results[identity][0].append(round(max(df[markers[0]]), 3))  # copier coller + changer 0 ou 1 pour correspondre aux marqueurs

# Sum up and writing file
    title = rf"{PATHS.RES}\rom_009.csv"
    columns = "identity,mean Pelvis x velocity,median Pelvis x velocity,std Pelvis x velocity\n"  # if new metric, add the column here

    with open(title, "w+") as f:
        lines = []
        lines.insert(0, columns)
        for id in identities_results:
            mean_pelvis = np.mean(identities_results[id][0])
            std_pelvis = np.std(identities_results[id][0])
            median_pelvis = np.median(identities_results[id][0])  # add your metric here (based on all repeats)

            new_line = f"{id},{round(mean_pelvis, 3)},{round(median_pelvis, 3)},{round(std_pelvis, 3)}\n"  # add the metric in new_line
            lines.append(new_line)

        for line in lines:
            f.write(line)

