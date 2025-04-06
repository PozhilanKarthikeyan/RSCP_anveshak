from rscp.frame_parser import Frame
from rscp.message import types
from typing import List, Type

class Sender:
    def __init__(self) -> None:
        pass

    def create_serialze(self,msg_cls: Type[types.MessageBase], *args, **kwargs):
        msg = msg_cls(*args, **kwargs)
        serialized = msg.serialize()
        return(serialized)
    
    # def crt_ack(self):
    #     self.body=self.create_serialze(types.Acknowledge)

    # def crt_armdis(self):
    #     self.body=self.create_serialze(types.ArmDisarm, True)

    def ack_frame(self):
        self.body=self.create_serialze(types.Acknowledge)
        self.frame=Frame.create(0x00,self.body)
        return(self.frame)

    def armdis_frame(self):
        self.body=self.create_serialze(types.ArmDisarm, True)
        self.frame=Frame.create(0x01,self.body)
        return(self.frame)
    
    def navigation_to_gps_frame(self):
        self.body=self.create_serialze(types.NavigateToGPS, 1.0, 2.0)
        self.frame=Frame.create(0x02,self.body)
        return(self.frame)
    
    def task_completed_frame(self):
        self.body=self.create_serialze(types.TaskFinished)
        self.frame=Frame.create(0x03,self.body)
        return(self.frame)
    
    # def setstage_frame(self):
    #     self.body = 
    
    def dedect_frame(self):
        self.body=self.create_serialze(types.Detection,3.1415,"green")
        self.frame=Frame.create(0x09,self.body)
        return(self.frame)

    def taskfinshed_frame(self):
        self.body=self.create_serialze(types.TaskFinished)
        self.frame=Frame.create(0x03,self.body)
        return(self.frame)


    

    

if __name__=="__main__":
    hi=Sender()
    hi.ack_frame()
    hi.armdis_frame() 
    # hi.dedect_frame()
    # hi.test_navigation_to_gps_frame() 
    # hi.taskfinshed_frame()  


