import os
import time

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
import pandas as pd

from flowdetect import MyKNN


class Conversition:
    myAddr = ""
    targetAddr = ""
    stream = 0
    smallDownStream = 0
    upStream = 0
    pStream = 0
    upBigStream = 0

    def __init__(self, addr1, addr2):
        self.myAddr = addr1
        self.targetAddr = addr2


def resolvePack(fileName, myAddr):
    conversitions = []
    # c = Conversition(myAddr, targetAddr)
    # conversitions.append(c)
    for (pkt_data, pkt_metadata,) in RawPcapReader(fileName):
        ether_pkt = Ether(pkt_data)

        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'.
            # We disregard those
            continue
        if ether_pkt.type != 0x0800:
            # disregard non-IPv4 packets
            continue
        ip_pkt = ether_pkt[IP]
        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue
        tcp_pkt = ip_pkt[TCP]
        flag = 0
        for c in conversitions:
            if c.myAddr == ip_pkt.src and c.targetAddr == ip_pkt.dst:
                c.stream += 1
                c.upStream += 1
                if 'P' in tcp_pkt.flags:
                    c.pStream += 1
                if ether_pkt.len >= 1000:
                    c.upBigStream += 1
                flag = 1
                break
            elif c.myAddr == ip_pkt.dst and c.targetAddr == ip_pkt.src:
                c.stream += 1
                if 'P' in tcp_pkt.flags:
                    c.pStream += 1
                if ether_pkt.len <= 100:
                    c.smallDownStream += 1
                flag = 1
                break
        if flag == 0:
            if ip_pkt.src == myAddr:
                c = Conversition(ip_pkt.src, ip_pkt.dst)
                c.stream += 1
                c.upStream += 1
                if 'P' in tcp_pkt.flags:
                    c.pStream += 1
                if ether_pkt.len >= 1000:
                    c.upBigStream += 1
                conversitions.append(c)
            elif ip_pkt.dst == myAddr:
                c = Conversition(ip_pkt.src, ip_pkt.dst)
                c.stream += 1
                if 'P' in tcp_pkt.flags:
                    c.pStream += 1
                if ether_pkt.len <= 100:
                    c.smallDownStream += 1
                conversitions.append(c)
    return conversitions


def getTrainningdata(myAddr, targetAddr, conversitions):
    l = []
    for c in conversitions:
        if c.stream == 0:
            continue
        cl = []
        cl.append(c.smallDownStream / c.stream)
        cl.append(c.upStream / c.stream)
        cl.append(c.pStream / c.stream)
        cl.append(c.upBigStream / c.stream)
        if c.myAddr == myAddr and c.targetAddr == targetAddr:
            cl.append("danger")
        else:
            cl.append("normal")
        cl.append(myAddr)
        cl.append(targetAddr)
        l.append(cl)
    # name = ['DownSmallStream', 'UpStream', 'PushStream', 'UpBigStream', 'lable']
    csv = pd.DataFrame(data=l)
    csv.to_csv("./t.csv", mode='a', header=False, index=False)


def train():
    # fileName = "2.pcap"
    filePath = "./dzh/"
    allFile = os.listdir(filePath)
    print(allFile)
    for fileName in allFile:
        print(fileName)
        if fileName == ".DS_Store":
            continue
        # myAddr = "10.21.196.121"
        # myAddr = "172.16.47.128"
        # myAddr = "10.122.209.235"
        # myAddr = "10.21.196.121"
        myAddr = "192.168.122.146"
        targetAdder = "122.51.19.183"
        conversitions = resolvePack(filePath + fileName, myAddr)
        getTrainningdata(myAddr, targetAdder, conversitions)


def getAnalyseData(myAddr, conversitions):
    if not os.path.exists('./csv/'):
        os.makedirs('./csv/')
    l = []
    for c in conversitions:
        if c.stream == 0:
            continue
        cl = []
        cl.append(c.smallDownStream / c.stream)
        cl.append(c.upStream / c.stream)
        cl.append(c.pStream / c.stream)
        cl.append(c.upBigStream / c.stream)
        cl.append('')
        cl.append(c.myAddr)
        cl.append(c.targetAddr)
        l.append(cl)
    # name = ['DownSmallStream', 'UpStream', 'PushStream', 'UpBigStream', 'lable']
    csv = pd.DataFrame(data=l)
    filePath = './csv/' + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.csv'
    csv.to_csv(filePath, header=False, index=False)
    return filePath


def analyse(filePath, myAddr):
    conversitions = resolvePack(filePath, myAddr)
    path = getAnalyseData(myAddr, conversitions)
    f = pd.read_csv(path)
    x_test = f.iloc[:, 0:4]
    study = MyKNN.MyKNN(None, None, x_test, None, True)
    study.predict()
    study.createpage(path)


if __name__ == '__main__':
    train()
    analyse(filePath="", myAddr="")
