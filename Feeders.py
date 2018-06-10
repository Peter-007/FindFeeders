#!/usr/bin/env python

# Feeder数据结构：
# { 标签ID1:物料ID1，标签ID2:物料ID2,... }

import pickle

class Feeders():
    
    def __init__(self,filename="feeder.dat"):
        self.dict_Feeders = {}
        self.fileName = filename
        if filename:
            self.loadFromFile()

    def insert(self, RfID, SapID):
        self.dict_Feeders[RfID] = SapID
        self.saveToFile()

    def findFeeders(self, SapID):
        RfIDs = []
        for k in self.dict_Feeders:
            if self.dict_Feeders[k] == SapID:
                RfIDs.append(k)
                
        return RfIDs

    def findFeeder(self, SapID):
        RfID = "N/A"
        for k in self.dict_Feeders:
            if self.dict_Feeders[k] == SapID:
                RfID = k

        return RfID


    # 点亮指定RfID的Feeder上的电子标签LED灯
    def showFeeder(self,RfID):
        pass


    def remove(self, RfID):
        if RfID in self.dict_Feeders:
            self.dict_Feeders.pop(RfID)
            self.saveToFile()

    def saveToFile(self):

        if not self.fileName:
            return

        try:
            out_file = open(str(self.fileName), 'wb')
        except IOError:
            print("There was an error opening \"%s\"" % self.fileName)
            return

        pickle.dump(self.dict_Feeders, out_file)
        out_file.close()

    def loadFromFile(self):

        if not self.fileName:
            return

        try:
            in_file = open(str(self.fileName), 'rb')
        except IOError:
            print("There was an error opening \"%s\"" % self.fileName)
            return

        self.dict_Feeders = pickle.load(in_file)
        in_file.close()

        if len(self.dict_Feeders) == 0:
            print("The file you are attempting to open contains no data.")


    def FakeFeeders(self):
        for i in range(1500):
            self.insert(str(i),str(i))
        print(self.dict_Feeders)


if __name__ == '__main__':
    feeder = Feeders()
    print(feeder.dict_Feeders)
    #feeder.FakeFeeders()
    feeder.insert('0105', '12345601')
    
    print(feeder.findFeeder('12345601'))
    print(feeder.findFeeder('0001'))
    #feeder.remove('0001-00000001')
    print(feeder.dict_Feeders)

    feeder.saveToFile()
    #feeder.loadFromFile()
