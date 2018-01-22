#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fritzconnection as fc
import sqlite3
import time
from threading import *


class DatabaseHandler:

    def __init__(self):
        self.conn = sqlite3.connect('FritzWatcher.db')
        self.c = self.conn.cursor()

    def insert(self, alist):
        dataset = []
        t = int(time.time())
        dataset.append(t)
        dataset.extend(alist)
        dtuple = tuple(dataset)
        print dtuple
        self.c.execute('INSERT INTO connectionData VALUES (?,?,?,?,?,?,?,?,?,?)', dtuple)
        self.disconnect()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()


class FritzBoxHandler:
    def __init__(self):
        self.conn = fc.FritzConnection(password='9959')

    def checkFritzStatus(self):
        try:
            self.conn.call_action('WANIPConnection', 'GetStatusInfo')
            return True
        except:
            return False

    def getNetworkSpeed(self):
        dlist = [0,0]
        try:
            d = self.conn.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
            dlist[0] = d['NewLayer1UpstreamMaxBitRate']
            dlist[1] = d['NewLayer1DownstreamMaxBitRate']
        except Exception as e:
            print e
        return dlist

    def getUptime(self):
        status = 0
        try:
            b = self.conn.call_action('WANIPConnection', 'GetStatusInfo')
            return b['NewUptime']
        except Exception as e:
            print e
        return status

    def getIpAdresses(self):
        status = ["0.0.0.0", "0::"]
        try:
            status[0] = self.conn.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress']
            status[1] = self.conn.call_action('WANIPConnection', 'X_AVM_DE_GetExternalIPv6Address')['NewExternalIPv6Address']
        except:
            pass
        return status

    def getSentReceived(self):
        status= [0,0]
        try:
            status[0] = self.conn.call_action('WANCommonInterfaceConfig', 'GetTotalBytesSent')['NewTotalBytesSent']
            status[1] = self.conn.call_action('WANCommonInterfaceConfig', 'GetTotalBytesReceived')['NewTotalBytesReceived']
            return status
        except:
            pass
        return status

    def getHostNumbers(self):
        status=[0,0]
        try:
            b = self.conn_call_action('Hosts','GetHostNumberOfEntries')['NewHostNumberOfEntries']
            status[1] = b
            a = 0
            for n in range(0,b):
                ax = a.call_action('Hosts','GetGenericHostEntry', NewIndex=n)
                if ax["NewActive"] == '0':
                    a += 1
            return status
        except:
            pass
        return status
