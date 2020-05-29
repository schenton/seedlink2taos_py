# -*- coding: utf-8 -*-
# 中国地震台网中心 陈通  2020年5月14日
import taos
import obspy
from obspy.core import read, UTCDateTime

class taosUtil(object):
    def __init__(self, ip, user, password, database):
        self.conn = taos.connect(host=ip, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()
        self.database = database

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.conn.close()

    def execute(self, sql):
        self.cursor.execute(sql)

    def inesrt_mseed_data(self, trace):
        # 获取设备信息 台网名、台站名、位置号、通道号
        net = trace.stats.network
        sta = trace.stats.station
        loc = trace.stats.location
        chn = trace.stats.channel

        # 获取数据包的起始时间
        st_time = trace.stats.starttime  # utcdatetime format
        st_time = int(st_time.timestamp * 1000)

        # 获取采样信息
        samp_num = len(trace)  # 采样点数量
        samp_rate = trace.stats.sampling_rate  # 采样率
        samp_interval = 1 / samp_rate * 1000  # 采样间隔

        if loc == "":  #
            loc = "-"  # 1.6.3用两个横杠，1.6.4用一个横杠。

        str_sql = "INSERT INTO %s.%s_%s_%s_%s USING seismometer TAGS(%s, %s,%s, %s) VALUES" % (self.database,
                                                                                               net,
                                                                                               sta,
                                                                                               trace.stats.location,
                                                                                               chn,
                                                                                               net,
                                                                                               sta,
                                                                                               loc,
                                                                                               chn)
        data = trace.data.tolist()
        for index, val in enumerate(data):
            str_val = " (%d,%d)" % (st_time + index * samp_interval, val)
            str_sql += str_val

        try:
            self.cursor.execute(str_sql)
        except Exception as e:
            print(e)
            print(str_sql)
        pass
