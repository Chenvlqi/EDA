# coding:utf-8
from scapy.all import *
from scapy.layers.tls.record import TLS
from Processing import analyse
import _thread
import time


class TLSExtension(object):
    pass


class TLSSniffer:

    def __init__(self):
        self.ifaces = NetworkInterfaceDict()
        self.iface = None
        self.ip = None
        ifaces.load()

    def selectIface(self):
        ifaces.show()
        print()
        index = input('请输入你要选择的网卡index，若抓取所有网卡数据包，请输入ALL\n>> ')
        if index == 'ALL':
            return
        if not index.isnumeric():
            print('输入有误')
            exit(0)
        else:
            for i in ifaces.data:
                if ifaces.data[i].win_index == int(index):
                    self.iface = ifaces.data[i].description
                    self.ip = ifaces.data[i].ip

    def start(self):
        if not os.path.exists('./pcap/'):
            os.makedirs('./pcap/')
        self.selectIface()
        load_layer("tls")
        while True:
            packets = sniff(iface=self.iface, prn=lambda x: x.summary(), timeout=20, lfilter=lambda x: TLS in x)
            pcapPath = './pcap/' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.pcap'
            wrpcap(pcapPath, packets)
            _thread.start_new_thread(analyse, (pcapPath, self.ip))


if __name__ == '__main__':
    sniffer = TLSSniffer()
    sniffer.start()
