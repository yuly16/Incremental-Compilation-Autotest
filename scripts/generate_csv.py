from copy import deepcopy

import regex as re
import pandas as pd

first_compilation = pd.DataFrame(
    columns=['benchmark', 'link', 'optimization', 'll code generation', 'native code compilation',
             'native code linking', 'total'])
later_compilation = pd.DataFrame(
    columns=['benchmark', 'link', 'optimization', 'll code generation', 'native code compilation',
             'native code linking', 'total'])

class Measurement:
    def __init__(self):
        self.data = {'benchmark': "",
                'phase': "",
                'link': 0,
                'optimization': 0,
                'll code generation': 0,
                'native code compilation': 0,
                'native code linking': 0,
                'total': 0}
    def clear(self):
        self.data = {'benchmark': "",
                'phase': "",
                'link': 0,
                'optimization': 0,
                'll code generation': 0,
                'native code compilation': 0,
                'native code linking': 0,
                'total': 0}


def parse(line):
    parser = {
        re.compile(r"(?<=test main class ).*"): "benchmark",
        re.compile(r".+?(?= PHASE)"): "phase",
        re.compile(r"(?<=\[info] Linking \()[0-9]+(?= ms\))"): "link",
        re.compile(r"(?<=\[info] Optimizing \(.+?\) \()[0-9]+(?= ms\))"): "optimization",
        re.compile(r"(?<=\[info] Generating intermediate code \()[0-9]+(?= ms\))"): "ll code generation",
        re.compile(r"(?<=\[info] Compiling to native code \()[0-9]+(?= ms\))"): "native code compilation",
        re.compile(r"(?<=\[info] Linking native code \(.+? gc, .+? lto\) \()[0-9]+(?= ms\))"): "native code linking",
        re.compile(r"(?<=\[info] Total \()[0-9]+(?= ms\))"): "total",
    }
    for p, k in parser.items():
        res = p.findall(line)
        if len(res) == 1:
            return {k: res[0]}
    return {}

def append_to_dataframe(d):
    global first_compilation
    global later_compilation
    data = deepcopy(d)
    if data["phase"] == "COMPILE":
        del data["phase"]
        first_compilation.loc[len(first_compilation.index)] = \
            list(data.values())
    elif data["phase"] == "EDIT":
        del data["phase"]
        later_compilation.loc[len(first_compilation.index)] = \
            list(data.values())

def main():
    enable = True
    current_benchmark = ""
    is_first = True
    measurement = Measurement()

    with open("result", "r") as f:
        f_lines = f.readlines()
        for line in f_lines:
            res = parse(line.strip())
            for k, v in res.items():
                if k == "benchmark":
                    current_benchmark = v
                elif k == "phase":
                    if v == "WARM UP" or v == "TRANSITION":
                        enable = False
                    else:
                        enable = True
                        if is_first:
                            is_first = False
                        else:
                            append_to_dataframe(measurement.data)
                        measurement.clear()
                        measurement.data["benchmark"] = current_benchmark
                        measurement.data[k] = v
                elif enable:
                    measurement.data[k] = v
    append_to_dataframe(measurement.data)
    first_compilation.to_csv("result-first.csv")
    later_compilation.to_csv("result-later.csv")




if __name__ == '__main__':
    main()
