from rscp.frame_parser import Frame, FrameParser
from rscp.message import types
from typing import List, Type
import io
import rscp.message.types as message_types
import serial
import rospy
from std_msgs.msg import Bool, Float32, Int8 
from navigation.msg import auto

class RSCP_Receiver:
    def __init__(self) -> None:
        rospy.init_node("drive")
        self.data=None

        self.rscp_data=auto()

        self.task_completed_sub= rospy.Subscriber("/task_completed", Int8, callback= self.task_completed_callback)
        self.detection_sub= rospy.Subscriber("/Dedection", Int8, callback= self.dedection_callback)

        self.rscp_data_pub=rospy.Publisher("/rscp_data",auto,queue_size=10)

        self.rx=bytearray()
        self.ser=serial.Serial('/dev/pts/10', baudrate=115200, timeout=None)
        # self.msg_id = -1 #default
        # self.password = "nandhu6838"
        if self.ser.is_open:
            print(f"Connected to {self.ser.name}")


    # def create_deserialize(self,msg_cls: Type[types.MessageBase], *args, **kwargs):
    #     msg = msg_cls(*args, **kwargs)
    #     deserialized = msg.deserialize(*args, **kwargs)
    #     print(deserialized)

    def task_completed_callback(self,check) :
        if check.data==1:
            self.frame=self.task_completed_frame()
            self.ser.write(self.frame)

    def dedection_callback(self,check):
        self.frame=self.dedect_frame()
        self.ser.write(self.frame)


    def on_update(self,frame):
        self.msg_id = frame.msg_id
        self.data=frame.data

        if frame.msg_id == 0:
            self.acknowledge_body()
            self.rx=bytearray()
            # self.frame=self.ack_frame()
            # self.ser.write(self.frame)

        elif frame.msg_id == 1:
            self.armdisarm_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 2:
            self.navigatetoGPS_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)


        elif frame.msg_id == 3:
            self.taskfinished_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 4:
            self.setstage_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)
            
        elif frame.msg_id == 5:
            self.text()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 6:
            self.arucotag_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 7:
            self.locatearucotags_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 8:
            self.locate3d_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 9:
            self.detection_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        elif frame.msg_id == 10:
            self.setparameters_body()
            self.rx=bytearray()
            self.frame=self.ack_frame()
            self.ser.write(self.frame)

        


    

    def test_parser(self,bytestream):
        # frame: bytes =bytestream
        self.rx.extend(bytestream)

        frame_parser = FrameParser(self.on_update)

        for byte in self.rx:
            frame_parser.process(byte)




    def acknowledge_body(self):
        self.body = types.Acknowledge.deserialize(self.data)
        return (self.body)
    
    def armdisarm_body(self):
        self.body=types.ArmDisarm.deserialize(self.data)
        self.rscp_data.arm=self.body.arm
        self.rscp_data_pub.publish(self.rscp_data)
        print(self.body.arm)
    
    def navigatetoGPS_body(self):
        self.body = types.NavigateToGPS.deserialize(self.data)

        self.rscp_data.latitude = self.body.latitude
        self.rscp_data.longitude = self.body.longitude
        self.rscp_data_pub.publish(self.rscp_data)

        print (self.body.latitude)

    
    def taskfinished_body(self):
        self.body = types.TaskFinished.deserialize(self.data)
        print(self.body)
    
    def setstage_body(self):
        self.body = types.SetStage.deserialize(self.data)

        self.rscp_data.setstage = self.body.stage_id
        self.rscp_data_pub.publish(self.rscp_data)

        print(self.body)
    
    def text(self):
        self.body = types.Text.deserialize(self.data)

        self.rscp_data.text = self.body.text
        self.rscp_data_pub.publish(self.rscp_data)

        print(self.body)
    
    
    def arucotag_body(self):
        self.body=types.ArucoTag.deserialize(self.data)
        
        
        
        print (self.body)
    
    def locatearucotags_body(self):
        self.body=types.LocateArucoTags.deserialize(self.data)
        
        self.rscp_data_pub.publish(self.rscp_data)
        
        print(self.body)
    
    def locate3d_body (self):
        self.body=types.Location3D.deserialize(self.data)

        self.rscp_data.reference = self.body.reference
        self.rscp_data.aruco_coordinates = [self.body.x ,self.body.y,self.body.z]
        self.rscp_data_pub.publish(self.rscp_data)

        print(self.body)
    
    def detection_body(self):
        self.body=types.Detection.deserialize(self.data)
        print(self.body)
    
    def setparameters_body(self):
        self.body=types.SetParameters.deserialize(self.data)
        return self.body

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
    
    def main(self):
        while(1):
            try:
                data = self.ser.read()  
                if data:
                    print(f"Received: {data}")
                    self.test_parser(data)
                else:
                    print("No data received within the timeout period.")
            except KeyboardInterrupt:
                print("Exiting...")
        

if __name__ == '__main__':
    RSCP_object = RSCP_Receiver()
    RSCP_object.main()
    rospy.spin()


    


