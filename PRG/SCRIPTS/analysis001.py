import os

import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis():
    """
    Get mean maximum angle, median angle, and std for the pelvis and the thorax while tying the shoes.
    """
    # Getting al the repeats for the exercise 001
    all_paths = ff.get_all_files(PATHS.XSENS)
    exercise = "001"
    sheet = "Ergonomic Joint Angles ZXY"
    markers = ["Vertical_Pelvis Flexion/Extension", "Vertical_T8 Flexion/Extension", ]  # add your marker
    all_repeats = []
    for p in all_paths:
        if exercise + "-repeat" in p and "AnKo" not in p: #and "DoMa" not in p: --> Si je veux que DoMa ne soit pas dans
            all_repeats.append(p)

    # Getting the different participating people
    identities = []
    for r in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(r))) # copier coller identity
        already_exist = False
        for id in identities:
            if identity in id:
                already_exist = True
        if not already_exist:
            identities.append(identity)

    # Defining and getting the metrics for all the repeats
    pelvis_maxima = []
    thorax_maxima = []  # add your values-containing list for your marker
    # copier coller tel quel dans toutes analayse + penser aux nombres de crochets !
    identities_results = {"003_DoMa": ([], []), "002_BaEl": ([], []), "004_LoJu": ([], []), "005_LuWi": ([], []),
                          "006_ReCo": ([], []), "007_AmVi": ([], []), "008_GuEm": ([], []), "009_ChCl": ([], []),
                          "010_AnKo": ([], []), "011_YaJu": ([], []), "012_PaMa": ([], []), "013_SaCl": ([], []),
                          "014_MoLu": ([], []), "015_LaJu": ([], []), "016_LaCh": ([], []), "017_GoMa": ([], []),
                          "018_FaFr": ([], []), "019_GuAl": ([], []), "020_PlSi": ([], []), "021_GuGi": ([], []),
                          "022_DrGe": ([], []), }

    for p in all_repeats:
        identity = os.path.basename(os.path.dirname(os.path.dirname(p))) # ajouter cette ligne
        df = pd.read_excel(p, sheet_name=sheet)

        identities_results[identity][0].append(round(max(df[markers[0]]), 3)) #copier coller + changer 0 ou 1 pour correspondre aux marqueurs
        identities_results[identity][1].append(round(max(df[markers[1]]), 3))
        # pelvis_maxima.append(round(max(df[markers[0]]), 3))
        # thorax_maxima.append(round(max(df[markers[1]]), 3))  # add the new metric in the previous defined list

    # Sum up and writing file
    title = rf"{PATHS.RES}\rom_001.csv"
    columns = "identity,mean maximum pelvis angle,median pelvis angle,std pelvis angle,mean maximum thorax angle," \
              "median thorax angle,std thorax angle\n"  # if new metric, add the column here

    with open(title, "w+") as f: #ouverture fichier
        lines = [] # initialisation de toutes les lignes
        lines.insert(0, columns) #ajouter 1ere ligne --> noms colonnes
        for id in identities_results: #pour chaque participants on va faire la boucle qui suit :
            mean_pelvis = np.mean(identities_results[id][0])   # de 64 à 70 : on calcule les métriques
            mean_thorax = np.mean(identities_results[id][1])
            std_pelvis = np.std(identities_results[id][0])
            std_thorax = np.std(identities_results[id][1])
            median_pelvis = np.median(identities_results[id][0])
            median_thorax = np.median(identities_results[id][1]) # add your metric here (based on all repeats)

            # 72/73 --> on créer la nouvelle ligne qu'on va ajouter
            new_line = f"{id},{round(mean_pelvis, 3)},{round(median_pelvis, 3)},{round(std_pelvis, 3)}," \
                f"{round(mean_thorax, 3)},{round(median_thorax, 3)},{round(std_thorax, 3)}\n"   # add the metric in new_line
            lines.append(new_line) #on ajoute notre nouvelle ligne à la liste de toutes les lignes
        for line in lines: #on parcourt toutes les lignes de notre liste
            f.write(line) # on écrit dans le fichier lignes par lignes
