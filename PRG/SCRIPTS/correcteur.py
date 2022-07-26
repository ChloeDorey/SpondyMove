import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import FireFiles as ff
import PATHS


def correction(manual_test=None, show=True):  # manual_test is a list of string, format : ["001_ChHo", "003_DoMa"]
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
    all_smooth = []
    all_rom_and_time = []

    for p in all_paths:
        if "smoothness" in p:
            all_smooth.append(p)
        if "rom" in p or "time" in p:
            all_rom_and_time.append(p)

    for p in all_rom_and_time:
        lines = []
        with open(p, "r") as f:
            lines = f.readlines()
        with open(p, "w+") as f:
            for line in lines:
                f.write(line.replace(",", "\t"))

    for p in all_smooth:
        lines = []
        elements = []
        corrected_lines = []
        in_list = False
        headers = ""
        with open(p, "r") as f:
            lines = f.readlines()
            headers = lines[0]
            corrected_lines.append(headers.replace(",", "\t"))
        for line in lines[1:]:
            line_elements = []
            element = ""
            for xc in range(len(line)):
                if line[xc] != "[" and not in_list:
                    element += line[xc]
                if line[xc] == "[" and not in_list:
                    in_list = True
                    elements += line[xc]
                    line_elements.append(element)
                    element = ""
                if line[xc] != "]" and in_list:
                    element += line[xc]
                if line[xc] == "]" and in_list:
                    in_list = False
                    element += line[xc]
                    line_elements.append(element.replace(",", "#"))
                    element = ""

            correct_line = ""
            for elem in line_elements:
                correct_line += elem.replace(",", "\t").replace("#", ",")

            corrected_lines.append(correct_line+ "\n")

        with open(p, "w+") as f:
            for new_line in corrected_lines:
                f.write(new_line)
