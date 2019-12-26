import subprocess
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    subprocess.check_output(["black", "-l", "100", "./"])

    # When using black on the directory, it only changes the files ending in .py. However, when
    # using flake or pylint in the same way, it walks the tree on files in pychache and venv.
    # Therefore, files ending in .py need to be found in the local directory. The problem is that
    # subprocess does not handle wildcards very well. I then need to use the lamda below to get
    # files, check they end in .py then apply flake8
    files = [f for f in listdir("./") if isfile(join("./", f))]
    for file in files:
        if file.endswith(".py"):
            # subprocess.check_output(["pylint", file])
            # subprocess.check_output(["flake8", file], shell=True)
            try:
                output = subprocess.check_output(
                    "flake8 " + file,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    timeout=3,
                    universal_newlines=True,
                )
            except subprocess.CalledProcessError as exc:
                print("Flake8 FAIL with error code: {}\n".format(exc.returncode), exc.output)
            else:
                if output != "":
                    print("Flake8 Output: {}".format(output))

            try:
                output = subprocess.check_output(
                    "Pylint " + file,
                    stderr=subprocess.STDOUT,
                    shell=True,
                    timeout=10,
                    universal_newlines=True,
                )
            except subprocess.CalledProcessError as exc:
                print("Pylint FAIL with error code: {}\n".format(exc.returncode), exc.output)
            else:
                if output != "":
                    print("Pylint Output: {}".format(output))
