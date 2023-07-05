import os, sys
if str(os.getenv('SST_DEV')).strip() == '1':
    os.system('pip uninstall -y streamsuperlit')       # removing the stable version
    sys.path.append('../src')                      # adding the development version

else:
    os.system('pip uninstall -y streamsuperlit')       # removing the stable version
    os.system('pip install -r requirements.txt')

from streamsuperlit.model import SSTCore
from streamsuperlit.core.utils import navigate

sst = SSTCore()
navigate('mainpage')