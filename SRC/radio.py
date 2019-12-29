class RadioStream:
    def __init__(self, path, hw_id, dest_id):
        self.file_path = path
        self.id = hw_id
        self.dest_id = dest_id

    #Strings are encoded with utf-8 and sent to the filestream where the radio program will send it
    def Send(self, data_id_tag, string):
        try:
            with open(self.file_path, 'wb+') as fl:
                fl.write(self.id)
                fl.write(self.dest_id)
                fl.write(b'\x00')
                fl.write(b'\x00')
                fl.write(data_id_tag)
                fl.write(string.encode('utf-8')) #from text to binary
            return True

        except:
            return False

    def SendBytes(self,data_id, bytes_var):
        try:            
            with open(self.file_path, 'wb+') as fl:
                fl.write(self.id)
                fl.write(self.dest_id)
                fl.write(b'\x00')
                fl.write(b'\x00')
                fl.write(data_id_tag)
                fl.write(bytes_var) #raw binary
            return True

        except:
            return False
