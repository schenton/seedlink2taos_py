# seedlink2taos_py
A Python program that fetches seismic waveform data from IRIS and writes to TDengine database.

## 程序说明

1. 简介：一个简化版的示例程序，从IRIS 获取MiniSeed地震数据，使用obspy将MiniSeed数据解包成采样点，并将采样点按照时间序列存入TDengine。
2. 需提前安装obspy包，可以通过`pip install obspy` 进行安装。 
3. 存入数据后，可使用grafana显示某个台站的地震波形。

## TDengine数据库 sql语句

在运行程序前，需要提前创建数据库和超级表

1. 创建数据库 create database seisflink;
2. 选择数据库 use seisflink;
3. 创建超级表 create table seismometer (ts TIMESTAMP, data INT) TAGS(net BINARY(20), sta BINARY(20), loc BINARY(20), chn BINARY(20) );
4. 每一个台站对应一张表。如seisflink.IU_ANMO_00_BHZ

## taos数据库相关

1. Windows下使用，请安装TDengine Windows client驱动，并将taos.dll taos.lib放入程序子lib文件夹。
2. Linux下使用，安装TDengine的Linux cline驱动

驱动下载地址https://www.taosdata.com/cn/getting-started/，源码地址：https://github.com/taosdata/TDengine
