import serial
import struct
from message_layer import Acknowledge,SensorData,id_to_class,TaskCompleted

class New_Protocol():
    def __init__(self,port_name,baud):
        self.serial_object=serial.Serial(port=port_name,baudrate=baud)
        self.start_byte=0X7E
        self.end_byte=0X7F
    def calculate_checksum(self,data):
        return sum(data) & 0xFF
    def create_frame(self,message_id,payload):
        payload_length =len(payload)
        frame = struct.pack('B', self.start_byte)
        frame += struct.pack('B', message_id)
        frame += struct.pack('B', payload_length)
        frame += payload
        checksum = self.calculate_checksum(frame[1:])  
        frame += struct.pack('B', checksum)
        frame += struct.pack('B', self.end_byte)
        return frame
    def send_frame(self, message_id, payload):
        frame = self.create_frame(message_id, payload)
        print(frame)
        self.serial_object.write(frame)
    def parse_frame(self,frame):
        if frame[0] != self.start_byte:
            raise ValueError("Invalid frame structure")
        message_id = frame[1]
        payload_length = frame[2]
        payload = frame[3:3+payload_length]
        checksum = frame[3+payload_length]
        if self.calculate_checksum(frame[1:3+payload_length]) != checksum:
            raise ValueError("Checksum mismatch")
        msg=self.handle_payload(payload,message_id)
        return (message_id,msg)
    
    def handle_payload(self,payload,msg_id):
        print("inside")
        cls=id_to_class[msg_id]
        print(cls)
        # print(payload,type(payload))
        # cls=TaskCompleted(True)
        msg=cls.deserialize(payload)
        print("after inside")
        return msg

    def receive_frame(self):
        data_array=bytearray()
        # print("step1")
        while True:
            # print("2")
            
            data=self.serial_object.read()
            print(data)
            if data==b'~':
                # data=self.serial_object.read(self.serial_object.in_waiting)
                data_array.extend(data)
                while (data!=b'\x7f'):
                    # print("4")
                    data=self.serial_object.read()
                    print(data)
                    data_array.extend(data)
                    # print(data_array)
                try:
                    # print("5")
                    message_id, msg = self.parse_frame(data_array)
                    return message_id, msg
                except ValueError as e:
                    print(f"Error: {e}")
                    continue

    def close_port(self):
        self.serial_object.close()