import zipfile
import os
import hashlib
from os.path import exists
from os.path import isfile


# Function that read a file
def read_file(fil):
    with open(fil, 'r') as f:
        try:
            data = f.read()
        except IOError:
            print("There is an error reading the file " + fil)
        finally:
            f.close()
    return data


# Add content at the end of a file
def add_content_file(fil, data):
    with open(fil, 'a') as f:
        try:
            f.writelines(data)
        except IOError:
            print("There is an error writing into the file " + fil)
        finally:
            f.close()


# Search a string inside a file
def search_str_file(fil, token):
    found = 0
    with open(fil, 'r') as f:
        try:
            data = f.read()
        except IOError:
            print("There is an error reading the file " + fil)
        if token in data:
            found = 1
    f.close()
    if found == 1:
        return True
    else:
        return False


# Unzip a file
def unzip_files(fil, dct):
    with zipfile.ZipFile(fil, "r") as zip_ref:
        try:
            zip_ref.extractall(dct)
        except IOError:
            print("There is an error unzipping " + fil)


# Check SHA of file
def check_sha(fil):
    buf_size = 65536
    shahash = hashlib.sha512()
    with open(fil, 'rb') as f:
        while True:
            try:
                data = f.read(buf_size)
            except IOError:
                print("There is an error reading the file " + fil)
            if not data:
                break
            shahash.update(data)

    shahashed = shahash.hexdigest()
    return shahashed


# Check if a directory exists
def check_dir(dct):
    pathisfile = os.path.isfile(dct)
    direxist = False
    if not pathisfile:
        try:
            direxist = os.path.isdir(dct)
        except IOError:
            print("There is an error with the directory " + dct + " path.\n")
    else:
        print("This is a file not a directory.\n")
    return direxist


# Check if a directory is empty
def check_dir_empty(path):
    pathisfile = os.path.isfile(path)
    pathexists = os.path.exists(path)

    if pathexists and not pathisfile:
        if not os.listdir(path):
            return True
        else:
            return False
    else:
        print("The path is either for a file or not valid.\n")


# Check if a file exists with full path
def check_file(path, fil):
    file_exists = False
    dir_exists = check_dir(path)
    if dir_exists:
        pathfil = os.path.join(path, fil)
        try:
            file_exists = exists(pathfil)
        except IOError:
            print("There is an error with the path, permissions or the file " + pathfil + " doesn't exists.\n")
    else:
        print(path + " is incorrect or doesn't exists.\n")
    return file_exists


# Create an empty file
def create_file(path, fil):
    fileexists = check_file(path, fil)
    if fileexists:
        print("Can't create the file " + fil + " because exists already on " + path + ".\n")
    else:
        pathfil = os.path.join(path, fil)
        try:
            open(pathfil, 'a').close()
        except IOError:
            print("There is an error creating the file " + pathlib)


# Create a directory
def create_dir(path, dct):
    pathdir = os.path.join(path, dct)
    try:
        os.mkdir(pathdir)
    except IOError:
        print("There is an error creating the dir " + dct + " on " + path)


# Remove a directory
def remove_dir(path, dct):
    pathdir = os.path.join(path, dct)
    try:
        os.rmdir(pathdir)
    except IOError:
        print("There is an error removing the dir " + dct + " on " + path)


# Remove a file
def remove_file(path, fil):
    pathfil = os.path.join(path, fil)
    try:
        os.remove(pathfil)
    except IOError:
        print("There is an error removing the file " + fil + " on " + path)


# Copy data in Windows OS
def copy_data_win(srcdir, targetdir):
    cmd = "xcopy /E /Y " + srcdir + " " + targetdir + "\\"
    print("Copying: " + cmd)
    print("Copying from " + srcdir + " to " + targetdir + ".\n")
    return cmd


# Check if a directory is writable
def directory_writable(dct):
    filerand = random.randint(1111111111, 9999999999)
    file = "test_" + str(filerand) + ".tst"
    dct = dct + "\\" + file
    f = ""
    try:
        f = open(cwd, 'w')
        dctwritable = True
    except IOError:
        dctwritable = False
    finally:
        f.close()
    os.remove(dct)
    return dctwritable


# Check if AWS CLI is installed
def aws_cli_installed():
    awsinstalled = os.system("aws --version")
    if awsinstalled == 0:
        return True
    else:
        return False


# Function used for checking if the file is empty or not
def check_empty_file(path):
    return os.path.isfile(path) and os.path.getsize(path) > 0


# File for reading from file an write to dictionary
def file_to_dict(fil, dct):
    with open(fil) as f:
        for line in f:
            if not line.startswith("#"):
                hashcount = line.count('=')
                if hashcount == 1:
                    (k, v) = line.split('=')
                    if not k.startswith("#"):
                        dct[str(k)] = v.strip('\n')
                else:
                    print("Wrong configuration in " + line)
