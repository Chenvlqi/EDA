# coding:utf-8
from scapy.all import *
from scapy.layers.tls.handshake import TLSClientHello
from scapy.layers.tls.record import TLS
import time


class TLSExtension(object):
    pass


class TLSSniffer:

    def __init__(self):
        self.ifaces = NetworkInterfaceDict()
        self.iface = None
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

    def processCap(self, fileName):
        packet = rdpcap(fileName)
        res_key = os.path.basename(fileName)
        res = {}
        extenList = []
        for item in packet:
            if item.haslayer(TLSClientHello):
                clienthello = item.getlayer(TLSClientHello)
                if clienthello.haslayer(TLSExtension):
                    extnum = len(clienthello.extensions)
                    for i in range(1, extnum + 1):
                        extension = clienthello.getlayer(TLSExtension, i)
                        exten = '{:04x}'.format(extension.type)
                        extenList.append(exten)
                break
        res[res_key] = extenList
        return res

    def main(self):
        self.selectIface()
        load_layer("tls")
        while True:
            packets = sniff(iface=self.iface, prn=lambda x: x.summary(), timeout=120, lfilter=lambda x: TLS in x)
            pcapName = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.pcap'
            wrpcap(pcapName, packets)


if __name__ == '__main__':
    sniffer = TLSSniffer()
    sniffer.main()
