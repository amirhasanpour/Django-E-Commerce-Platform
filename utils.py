def create_random_code(count):
    import random
    count -= 1
    return random.randint(10**count, 10**(count+1)-1)



# import ghasedakpack
def send_sms(mobile_number, messages):
    pass
    # try:
    #     sms = ghasedakpack.Ghasedak("64b028bdcfea1517740d4c4938ca35ae8242105d9600f85aac1a9268648aefa6")
    #     sms.verification({'receptor': str(mobile_number),'type': '1','template': 'randcode','param1': str(messages)})
    # except Exception as error:
    #     print(f"Error is : {error}")
    
    
    
import os
from uuid import uuid4

class FileUpload:
    def __init__(self, dir, prefix):
        self.dir = dir
        self.prefix = prefix
        
    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"