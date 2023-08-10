import socket
import json

import ServerException

SERVER_FAULT = "server_fault"

exception_message_table = {
    # Invalid Queue size
    ServerException.InvalidQueueSize : SERVER_FAULT, 
    # Invalid server configuration file keys
    ServerException.InvalidConfig : SERVER_FAULT, 
    # Full server queue
    ServerException.QueueFull : "503", 
}

class Core:
    """
    
    Core 
        A class generates a simple server. 

    Example
        server = Core()
        server.load_config()
        server.retrieve_config()
        server.listen()
        server.save_config() # currently not working. 
    
    
    load_config
    \- _validate_dict_keys
    save_config
    config_to_str
    retrieve_config

    """
    def __init__(self):
        # Configuration related fields
        self.config_path = "./server_config.json"
        self.config = dict()
        self.config_key = ["port", "connect_limit"]

        # Server configuration fields
        self.port = None
        self.connect_limit = None

    def _validate_dict_keys(self, origin: list, target: dict) -> bool:
        """
            _validate_dict_keys
                A function checks if the keys in configuration file are known to self.config_key. 

            parameters
                origin ('list')
                    A 'list' of 'str' including configuration name keys for server. 
            
            returns
                'bool'
                    True if the keys are valid,
                    False if there are some keys that are not known to self.config_key 
        """

        # Union set of origin and target
        validator = [k for k in origin if k in target.keys()]
        return len(validator) == len(origin) and len(validator) == len(target)
    
    def load_config(self) -> None:
        """
            load_config
                A function
        """
        with open(self.config_path, "r", encoding="UTF-8") as f:
            cf = json.load(f)

            # Check if dict from the configuration file and 
            # program configuration have the same key set. 
            if not self._validate_dict_keys(self.config_key, cf):
                raise ServerException.InvalidConfig
            
        self.config = cf

    def retrieve_config(self) -> None:
        """
            retrive_config
                A function registers configuration values to the server's fields. 
                
            parameters
                
            returns

        """
        for k in self.config_key:
            setattr(self, k, self.config[k])

    def save_config(self) -> None:
        """
            save_config
                A function saves server configurations as a json file.

            parameters

            returns
        
        """
        with open(self.config_path, "w", encoding="UTF-8") as f:
            json.dump(self.config, f, indent=4)

    def _config_to_str(self) -> str:
        """
            _config_to_str
                A function prints server configurations as a text. 

            parameters

            returns

        """
        config = list()

        for k in self.config.keys():
            config.append(f"{k:20} : {self.config[k]: 40}")

        return "\n".join(config)
    
    def listen(self):
        """
            listen
                A function accepts socket connections

            parameters

            returns

            
        """
        br_request = []
        nconnect = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', self.port))
            s.listen(self.connect_limit)
            
            while True:
                conn, addr = s.accept()
                with conn:
                    print("from: ", addr)
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        br_request.append(str(data))
        
                with open(f"./brower_request{nconnect:1}.txt", "w", encoding="UTF-8") as f:
                    "".join(br_request)
                    f.write(str(br_request[0]))
                nconnect += 1