import struct

class MessageBase():
    def __init__(self,msg_id):
        self.msg_id=msg_id

    def serialize(self):
        raise NotImplementedError
    
    def deserialize(self):
        raise NotImplementedError
    

class Acknowledge(MessageBase):
    def __init__(self):
        super().__init__(msg_id=0x0)

    def serialize(self):
        return b""
    
    @staticmethod
    def deserialize(data):
        assert len(data)==0
        return Acknowledge()
    

class SensorData(MessageBase):
    def __init__(self,imu_data,latitude,longitude):
        super().__init__(msg_id=0x01)
        self.imu_data=imu_data
        self.latitude=latitude
        self.longitutde=longitude

    def serialize(self):
        return struct.pack(">fff",self.imu_data,self.latitude,self.longitutde)
    
    @staticmethod
    def deserialize(data):
        # print(len(data))
        imu_data,latitude,longitude=struct.unpack(">fff",data)
        return SensorData(imu_data,latitude,longitude)
    
class TaskCompleted(MessageBase):
    def __init__(self,bool):
        super().__init__(msg_id=0x02)
        self.bool=bool
    
    def serialize(self):
        return struct.pack(">?",self.bool)
    
    @staticmethod
    def deserialize(data):
        print("before test")
        assert len(data)==1 
        print("test")
        bool=struct.unpack(">?",data)
        return TaskCompleted(bool)
    

id_to_class:dict[int,MessageBase]={0x00:Acknowledge,0x01:SensorData,0x02:TaskCompleted}
Class_to_id={Acknowledge:0x00,SensorData:0x01,TaskCompleted:0x02}