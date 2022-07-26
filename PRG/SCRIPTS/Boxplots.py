import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import FireFiles as ff
import PATHS
import ast


def analysis(manual_test=None, show=True):  # manual_test is a list of string, format : ["001_ChHo", "003_DoMa"]
    if manual_test is None:
        manual_test = []
    all_paths = []
    if len(manual_test) != 0:
        print(f"doing analysis on {manual_test}")
        intermediate_paths = ff.get_all_files(PATHS.RES)
        for p in intermediate_paths:
            for m in manual_test:
                if m in p and ".csv" in p:
                    all_paths.append(p)
    else:
        all_paths = ff.get_all_files(PATHS.RES)
    rom_paths = []
    smooth_paths = []
    small_smooth_paths = []
    small_paths = []

    time_paths = []
    for p in all_paths:
        if "rom" in p and "007" not in p and "009" not in p:
            rom_paths.append(p)
        if "smooth" in p and "001" not in p and "004" not in p:
            smooth_paths.append(p)
        if "smooth" in p and ("001" in p or "004" in p):
            small_smooth_paths.append(p)
        if "007" in p or "009" in p:
            small_paths.append(p)
        if "time" in p:
            time_paths.append(p)

    figrom, axrom = plt.subplots(1, 1)
    for x in range(len(rom_paths)):
        print(rom_paths[x])
        exercise = os.path.basename(rom_paths[x]).split(".")[0].split("_")[1]
        df = pd.read_csv(rom_paths[x], sep="\t")
        df = df.dropna(axis=0)

        data = df[df.columns[1]].to_list()
        axrom.boxplot(data, vert=False, labels=[exercise, ], positions=[x, ])
        title = "rom à compléter"
        xlabel = "rom à compléter"
        ylabel = "rom à compléter"
        axrom.set_title(title)
        axrom.set_xlabel(xlabel)
        axrom.set_ylabel(ylabel)
        plt.savefig(PATHS.RES + r"\rom boxplot.png")

    figsmooth, axsmooth = plt.subplots(1, 1)
    for x in range(len(smooth_paths)):
        print(smooth_paths[x])
        exercise = os.path.basename(smooth_paths[x]).split(".")[0].split("_")[1]
        df = pd.read_csv(smooth_paths[x], sep="\t")
        df = df.dropna(axis=0)

        data = []
        for row in df[df.columns[1]]:
            data.append(ast.literal_eval(row)[0])
        axsmooth.boxplot(data, vert=False, labels=[exercise, ], positions=[x, ])
        title = "smooth à compléter"
        xlabel = "smooth à compléter"
        ylabel = "smooth à compléter"
        axsmooth.set_title(title)
        axsmooth.set_xlabel(xlabel)
        axsmooth.set_ylabel(ylabel)
        plt.savefig(PATHS.RES + r"\smooth boxplot.png")

    figsmallsmooth, axsmallsmooth = plt.subplots(1, 1)
    for x in range(len(small_smooth_paths)):
        print(small_smooth_paths[x])
        exercise = os.path.basename(small_smooth_paths[x]).split(".")[0].split("_")[1]
        df = pd.read_csv(small_smooth_paths[x], sep="\t")
        df = df.dropna(axis=0)

        data = []
        for row in df[df.columns[1]]:
            data.append(ast.literal_eval(row)[0])
        axsmallsmooth.boxplot(data, vert=False, labels=[exercise, ], positions=[x, ])
        title = "smallsmooth à compléter"
        xlabel = "smallsmooth à compléter"
        ylabel = "smallsmooth à compléter"
        axsmallsmooth.set_title(title)
        axsmallsmooth.set_xlabel(xlabel)
        axsmallsmooth.set_ylabel(ylabel)
        plt.savefig(PATHS.RES + r"\smallsmooth boxplot.png")

    figtime, axtime = plt.subplots(1, 1)
    for x in range(len(time_paths)):
        print(time_paths[x])
        exercise = os.path.basename(time_paths[x]).split(".")[0].split("_")[1]
        df = pd.read_csv(time_paths[x], sep="\t")
        df = df.dropna(axis=0)

        data = df[df.columns[1]].to_list()
        axtime.boxplot(data, vert=False, labels=[exercise, ], positions=[x, ])
        title = "time à compléter"
        xlabel = "time à compléter"
        ylabel = "time à compléter"
        axtime.set_title(title)
        axtime.set_xlabel(xlabel)
        axtime.set_ylabel(ylabel)
        plt.savefig(PATHS.RES + r"\time boxplot.png")

    if show:
        plt.show()
