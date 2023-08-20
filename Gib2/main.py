import zipfile as z
import os
from sys import argv, stderr
import tempfile

cwd = os.getcwd()
tmpdir = tempfile.gettempdir()+"/gib"
tmp = []
commands = ["new",
            "get_commit"]

def new(name, path):
    rootlen = len(path) + 1
    with z.ZipFile(f"{name}.gib", "w") as master:
        with open("lastest_commit", "w") as f:
            tmp.append("lastest_commit")
            f.write("1")
        with z.ZipFile(f"1.zip", "w") as zip:
            tmp.append("1.zip")
            for base, dirs, files in os.walk(path):
                for file in files:
                    file = file
                    fn = os.path.join(base, file)
                    zip.write(fn, fn.removeprefix(path))
            try: os.makedirs(tmpdir+"/.gib/")
            except FileExistsError: pass
            with open("description", "w+") as f:
                tmp.append("description")
                f.write("Initial Commit\nInitial Commit for this Gib Box")
            os.chdir(tmpdir)
            zip.write(".gib/")
            os.chdir(cwd)
            zip.write("description", ".gib/description")
        master.write("1.zip")
        master.write("lastest_commit")
        for t in tmp:
            os.remove(t)

def get_commit(box, number):
    with z.ZipFile(f"{box}.gib", "r") as master:
        master.extract("lastest_commit")
        tmp.append("lastest_commit")
        master.extract(f"{number}.zip")
        tmp.append(f"{number}.zip")
        with z.ZipFile(f"{number}.zip", "r") as zip:
            zip.extract(".gib/description")
            tmp.append(".gib/description")
            with open(".gib/description", "r+") as d:
                ls = d.readlines()
                lines = []
                for i in ls:
                    lines.append(i.removesuffix("\n"))
                title = lines.pop(0)
                print("Title:", title)
                print("Description:")
                for i in lines:
                    print(i)
    for t in tmp:
        os.remove(t)

def main():
    args = []
    x = ""
    for i in range(len(argv)):
        if argv[i].startswith('"'):
            for i in argv[i:]:
                x += argv[i]
                if i.endswith('"'):
                    args.append(x)
                    break
        else:
            args.append(argv[i])
    if len(args) >= 2:
        if args[1] == commands[0]:
            new(args[2], args[3])
        if args[1] == commands[1]:
            get_commit(args[2], args[3])
    else:
        print("Gib needs more arguments to work", file=stderr)

if __name__ == "__main__":
    main()