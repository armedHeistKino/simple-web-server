class QueueFull(Exception):
    def __str__(self):
        return "Queue is Full. Request later. "
    
class InvalidQueueSize(Exception):
    def __str__(self):
        return "Invalid queue size. Server fault. "
    
class InvalidConfig(Exception):
    def __str__(self):
        return "Invalid server configuration. Server fault. "