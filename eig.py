import sys, os
import numpy as np


def main():
    args = sys.argv
    if len(args) != 2:
        # args[0] is this script file name
        raise RuntimeError("Only one argument is required.")
    filepath = args[1]
    if not os.path.isfile(filepath):
        raise RuntimeError(f"No such file: {filepath}")
    eigs = calc_eig_from_dat(filepath)
    [head, ext] = os.path.splitext(filepath)
    output_filepath = f"{head}_eig{ext}"
    write_eig(output_filepath, eigs)


def calc_eig_from_dat(fname):
    eigs = []
    with open(fname) as f:
        for i, line in enumerate(f):
            if line.startswith("#"):
                # skip comment line
                continue
            matrix = line2matrix(i, line)
            w, v = np.linalg.eig(matrix)
            eigs.append([w, v])
    return eigs


def line2matrix(i, line):
    components = line.split()
    # Frame, RoG, RoG[Max], XX, YY, ZZ, XY, XZ, YZ
    # Symmetric matrix. Use only the back six.
    if len(components) != 9:
        raise RuntimeError(f"Invalid data format at L{i}: {line}")
    [XX, YY, ZZ, XY, XZ, YZ] = map(float, components[3:9])
    matrix = np.array([[XX, XY, XZ], [XY, YY, YZ], [XZ, YZ, ZZ]])
    return matrix


def write_eig(fname, eigs):
    with open(fname, "w") as f:
        f.write(
            "%8s %10s %10s %10s %32s %32s %32s\n"
            % (
                "#Frame",
                "λ1",
                "λ2",
                "λ3",
                "v1",
                "v2",
                "v3",
            )
        )
        for i, [w, v] in enumerate(eigs):
            # i is 0-index
            frame = i + 1
            template_lambda = "%10.4f"
            template_vector = "%10.4f %10.4f %10.4f"
            l1 = template_lambda % w[0]
            l2 = template_lambda % w[1]
            l3 = template_lambda % w[1]
            v1 = template_vector % (v[0][0], v[0][1], v[0][2])
            v2 = template_vector % (v[1][0], v[1][1], v[1][2])
            v3 = template_vector % (v[2][0], v[2][1], v[2][2])
            line = "%8d %s %s %s %s %s %s\n" % (frame, l1, l2, l3, v1, v2, v3)
            f.write(line)


if __name__ == "__main__":
    main()
