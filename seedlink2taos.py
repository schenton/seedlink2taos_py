# -*- coding: utf-8 -*-
###############################################
#   将seedlink的 波形数据写入taos数据库
###############################################
# 中国地震台网中心 陈通  2020年5月14日

from taosUtil import taosUtil
from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient

class MySeedlinkClient(EasySeedLinkClient):
    def __init__(self, seedlinkserver):
        # 重载父类的init函数，用于从seedlink接收地震数据
        super(MySeedlinkClient, self).__init__(seedlinkserver)

        # tdengine地址。写入seisflink数据库（如果没有，需创建），参见readme 创建数据库和超级表。
        try:
            self.taosCon = taosUtil('172.27.140.219', 'root', 'taosdata', 'seisflink')
        except Exception as e:
            print(e)

    # Implement the on_data callback
    def on_data(self, trace):
        self.taosCon.inesrt_mseed_data(trace)
        print('Received trace:')
        print(trace)


def main():
    client = MySeedlinkClient('rtserve.iris.washington.edu:18000')

    # Select a stream and start receiving data
    # 只接入两个台站的数据，也可以根据需要接入更多数据
    client.select_stream('IU', 'ANMO', 'BHZ')
    client.select_stream('IU', 'ADK', 'BHZ')

    client.run()


if __name__ == '__main__':
    main()
