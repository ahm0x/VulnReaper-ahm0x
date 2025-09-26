if sys.platform.startswith("win"):
    print("Installing the python modules required for VulnReaper by ahm0x:")
    os.system("cls")
    os.system("python -m pip install --upgrade pip")
    os.system("python -m pip install -r requirements.txt")
elif sys.platform.startswith("linux"):
    print("Installing the python modules required for VulnReaper by ahm0x:")
    os.system("clear")
    os.system("python3 -m pip3 install --upgrade pip")
    os.system("python3 -m pip3 install -r requirements.txt")