import os, sys

DEBUG = True

if __name__ == "__main__":
    if DEBUG:
        os.system('pip uninstall -y streamsuperlit')       # removing the stable version
        sys.path.append('../src')                          # adding the development version
    else:
        os.system('pip uninstall -y streamsuperlit')       # reinstalling the stable version
        os.system('pip install -r requirements.txt')       # reinstalling the stable version

    from streamsuperlit import SSTCore, navigate

    sst = SSTCore()
    navigate('mainpage')