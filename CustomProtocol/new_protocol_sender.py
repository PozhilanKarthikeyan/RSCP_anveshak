from Basic_layer import New_Protocol
from message_layer import Acknowledge,TaskCompleted,SensorData
if __name__=="__main__":
    sender_object=New_Protocol("COM5",115200)
    try:
        # msg=Acknowledge()
        msg=TaskCompleted(False)
        # msg=SensorData([10.0,10,10,10,10,10],11.0,12.0)
        # msg=SensorData(10,11.0,12.0)
        sender_object.send_frame(0x02,msg.serialize())
    finally:
        sender_object.close_port
            