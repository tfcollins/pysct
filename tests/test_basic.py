import pytest
from pysct.core import Vivado, XsctServer, Xsct

vivado_version = '2019.1'

def test_interp():
    vivadoPath = "/opt/Xilinx/Vivado/"+vivado_version+"/bin/vivado"
    vivado = Vivado(vivadoPath, prompt='%')
    vivado.waitStartup()
    vivado.set_var('a', '5')
    assert vivado.get_var('a') == '5'
    vivado.exit()

def test_xsdb():
    PORT = 4567
    path = "/opt/Xilinx/SDK/"+vivado_version+"/bin/xsdb"
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
    path = "/opt/Xilinx/SDK/"+vivado_version+"/bin/xsdb"
    xsct_server = XsctServer(path, port=PORT, verbose=True)
    import time
    time.sleep(3)
    xsct = Xsct('localhost', PORT)
    print(xsct.do('connect'))
    time.sleep(3)
    print(xsct.do('targets'))
    time.sleep(3)
    print(xsct.do('targets 2'))
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

def test_jtag_load_sys_bad_sd():
    PORT = 4567
    path = "/opt/Xilinx/SDK/"+vivado_version+"/bin/xsdb"
    xsct_server = XsctServer(path, port=PORT, verbose=True)
    import time
    time.sleep(3)
    xsct = Xsct('localhost', PORT)
    print(xsct.do('connect'))
    time.sleep(3)
    print(xsct.do('targets'))
    time.sleep(3)
    print(xsct.do('target 1'))
    time.sleep(3)
    print(xsct.do('rst -system'))
    time.sleep(1)
    print(xsct.do('con'))
    time.sleep(1)

    import pathlib
    cw = pathlib.Path(__file__).parent.absolute()
    cw = str(cw)
    print(cw)

    print(xsct.do('target 2'))
    time.sleep(1)
    print(xsct.do('dow '+cw+'/resources/fsbl.elf'))
    time.sleep(1)
    print(xsct.do('con'))
    time.sleep(1)
    print(xsct.do('dow '+cw+'/resources/u-boot-zc70x.elf'))
    time.sleep(1)
    print(xsct.do('con'))
    time.sleep(7)
    print(xsct.do('target 1'))
    time.sleep(1)
    print(xsct.do('stop'))
    time.sleep(3)
    print(xsct.do('fpga -file '+cw+'/resources/system_top.bit'))
    time.sleep(1)
    print(xsct.do('dow -data '+cw+'/resources/devicetree.dtb 0x2A00000'))
    time.sleep(1)
    print(xsct.do('dow -data '+cw+'/resources/uImage 0x3000000'))
    time.sleep(1)
    print(xsct.do('con'))
    time.sleep(3)
    xsct.close()
    time.sleep(3)
    xsct_server.stop_server()
    print("System should be at u-boot menu")



def test_jtag_load_sys():
    PORT = 4567
    path = "/opt/Xilinx/SDK/"+vivado_version+"/bin/xsdb"
    xsct_server = XsctServer(path, port=PORT, verbose=True)
    import time
    time.sleep(3)
    xsct = Xsct('localhost', PORT)
    print(xsct.do('connect'))
    time.sleep(3)
    print(xsct.do('targets'))
    time.sleep(3)
    print(xsct.do('target 1'))
    time.sleep(3)
    print(xsct.do('rst -system'))
    time.sleep(1)

    import pathlib
    cw = pathlib.Path(__file__).parent.absolute()
    cw = str(cw)
    print(cw)

    print(xsct.do('target 2'))
    time.sleep(1)
    print(xsct.do('dow '+cw+'/resources/fsbl.elf'))
    time.sleep(1)
    print(xsct.do('con'))
    time.sleep(1)
    print(xsct.do('stop'))
    time.sleep(3)
    print(xsct.do('fpga -file '+cw+'/resources/system_top.bit'))
    time.sleep(1)
    print(xsct.do('dow -data '+cw+'/resources/devicetree.dtb 0x2A00000'))
    time.sleep(1)

    print(xsct.do('dow -data '+cw+'/resources/uImage 0x3000000'))
    time.sleep(1)
    print(xsct.do('dow '+cw+'/resources/u-boot-zc70x.elf'))
    time.sleep(1)

    print(xsct.do('con'))
    time.sleep(3)
    xsct.close()
    time.sleep(3)
    xsct_server.stop_server()



