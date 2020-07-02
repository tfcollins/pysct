import pytest
from pysct.core import Vivado, XsctServer, Xsct

def test_interp():
    vivadoPath = '/opt/Xilinx/Vivado/2019.1/bin/vivado'
    vivado = Vivado(vivadoPath, prompt='%')
    vivado.waitStartup()
    vivado.set_var('a', '5')
    assert vivado.get_var('a') == '5'
    vivado.exit()

def test_xsdb():
    PORT = 4567
    path = "/opt/Xilinx/SDK/2019.1/bin/xsdb"
    xsct_server = XsctServer(path, port=PORT, verbose=True)
    import time
    time.sleep(3)
    xsct = Xsct('localhost', PORT)
    print("xsct's pid: {}".format(xsct.do('pid')))
    print(xsct.do('set a 5'))
    print(xsct.do('set b 4'))
    print("5+4={}".format(xsct.do('expr $a + $b')))
    time.sleep(3)
    xsct.close()
    time.sleep(3)
    xsct_server.stop_server()

def test_jtag_reset():
    PORT = 4567
    path = "/opt/Xilinx/SDK/2019.1/bin/xsdb"
    xsct_server = XsctServer(path, port=PORT, verbose=True)
    import time
    time.sleep(3)
    xsct = Xsct('localhost', PORT)
    print(xsct.do('connect'))
    time.sleep(3)
    print(xsct.do('targets'))
    time.sleep(3)
    print(xsct.do('targets 1'))
    time.sleep(3)
    print(xsct.do('rst -system'))
    time.sleep(3)
    print(xsct.do('con'))
    time.sleep(3)
    print(xsct.do('stop'))
    time.sleep(3)
    print(xsct.do('con'))
    time.sleep(3)
    xsct.close()
    time.sleep(3)
    xsct_server.stop_server()

