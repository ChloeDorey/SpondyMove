import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import FireFiles as ff
import PATHS


def analysis(manual_test=None, show=True):  # manual_test is a list of string, format : ["001_ChHo", "003_DoMa"]
    if manual_test is None:
        manual_test = []
    all_paths = []
    if len(manual_test) != 0:
        print(f"doing analysis on {manual_test}")
        intermediate_paths = ff.get_all_files(PATHS.XSENS)
        for p in intermediate_paths:
            for m in manual_test:
                if m in p:
                    all_paths.append(p)
    else:
        all_paths = ff.get_all_files(PATHS.XSENS)

    exercise = ["001", "002", "003", "005", "006", "007", "010"]
    exercise_names = {"001": "Faire ses lacets", "002": "Ramasser un objet", "003": "Marches d'escaliers",
                      "005": "Inclinaison latérale ", "006": "Inclinaison latérale ", "007": "Flexion du tronc du tronc ",
                      "010": "Extension du tronc"}
    sheet = "Ergonomic Joint Angles ZXY"
    exercise_markers = {"001": "Vertical_Pelvis Flexion/Extension", "002": "Vertical_Pelvis Flexion/Extension",
                        "003": "Vertical_Pelvis Flexion/Extension", "005": "Vertical_Pelvis Lateral Bending",
                        "006": "Vertical_Pelvis Lateral Bending", "007": "Vertical_Pelvis Flexion/Extension",
                        "010": "Vertical_Pelvis Flexion/Extension"}  # add your markers here
    all_repeats = []
    for p in all_paths:
        for ex in exercise:
            if ex + "-repeat" in p:
                all_repeats.append(p)

    fig, ax = plt.subplots(3, 3, figsize=(10, 8))
    nrow = 0
    ncol = 0
    max_col = 2
    for ex in exercise:
        identities = []
        repeats_exercise = []
        for r in all_repeats:
            identity = os.path.basename(os.path.dirname(os.path.dirname(r)))

            if identity not in identities:
                identities.append(identity)

            if ex == os.path.basename(r).split("-")[0]:
                repeats_exercise.append(r)

        n_people = len(identities)
        angles = []
        for p in repeats_exercise:
            df = pd.read_excel(p, sheet_name=sheet)
            angles.append(df[exercise_markers[ex]])
            # plt.plot(df[markers[0]])

        arrays = [np.array(x) for x in angles]
        mean_angles = [np.mean(k) for k in zip(*arrays)]
        std_angles = [np.std(k) for k in zip(*arrays)]
        x_values = [x for x in range(len(mean_angles))]
        low_std = [mean_angles[x] - std_angles[x] for x in x_values]
        high_std = [mean_angles[x] + std_angles[x] for x in x_values]
        ax[nrow, ncol].plot(mean_angles, color="red", label="mean")
        ax[nrow, ncol].fill_between(x_values, low_std, high_std, color="black", alpha=.3, label="std")
        ax[nrow, ncol].set_title(f"{exercise_names[ex]} - n={n_people}")
        handles, labels = ax[nrow, ncol].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center')
        if ncol < max_col:
            ncol += 1
        else:
            ncol = 0
            nrow += 1

    plt.tight_layout()
    plt.savefig(PATHS.ROM)
    if show:
        plt.show()
        plt.close()
    else:
        plt.close()
