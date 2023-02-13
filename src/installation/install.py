#! /usr/bin/python3
import getpass
import subprocess
import re

# Returns host OS
def CheckOS():
    p = subprocess.run(["cat", "/etc/os-release"], capture_output=True)
    extractSysVars = p.stdout
    foundOS = re.findall('ID=(\w+)', str(extractSysVars))

    return foundOS[0]


# Creates the specified python environment. Returns None.
def CreateEnv(foundOS, passUser, envName="MainEnv"):

    relationEnv = {"fedora": ["dnf", ""],
                   "ubuntu": ["apt", "3"],
                   "raspbian": ["apt", "3"]}

    commonParams = {"text": True, "check": True, "stdout": subprocess.DEVNULL}

    try:
        print("Updating repositories...")
        p1 = subprocess.run(["sudo", "-S", f"{relationEnv[foundOS][0]}", "update"], input=passUser, **commonParams)
        print("OK\n" if p1.returncode == 0 else "Error")

        print("Verifying/Installing environment package...")
        p2 = subprocess.run(["sudo", "-S", f"{relationEnv[foundOS][0]}", "install", "-y",f"python{relationEnv[foundOS][1]}-virtualenv"], input=passUser, **commonParams)
        print("OK\n" if p2.returncode == 0 else "Error")

        print("Creating environment...")
        p3 = subprocess.run([f"python{relationEnv[foundOS][1]}", "-m", "venv", f"{envName}"], **commonParams)
        print("OK\n" if p3.returncode == 0 else "Error")

        print("Activating environment and installing dependencies...")
        p4 = subprocess.run(f"source {envName}/bin/activate && pip{relationEnv[foundOS][1]} install -r requirements.txt", shell=True, executable="/bin/bash", **commonParams)
        print("OK\n" if p4.returncode == 0 else "Error")

        print("Environment created! Check that everything is correct")

    except subprocess.CalledProcessError:
        raise Exception("Wrong root password entered")


def PrepareApp():
    return


if __name__ == "__main__":
    #envName = input("Enter the name of the virtual environment to create: ")
    passUser = getpass.getpass("Enter your root password: ")
    foundOS = CheckOS()
    envManaged = CreateEnv(foundOS.lower(), passUser)
