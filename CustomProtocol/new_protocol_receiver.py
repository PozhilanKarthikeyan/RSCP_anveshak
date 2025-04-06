from Basic_layer import New_Protocol

if __name__=="__main__":
    receiver_object=New_Protocol("COM6",115200)
    while(True):
        try:
            message_id, payload = receiver_object.receive_frame()
            print(f"Received message_id: {message_id}, payload: {payload}")
        except Exception as e:
            print(e)
            receiver_object.close_port()
            break
            
