import runpod
import time  
import os 

def handler(event):
    print(f"Worker Start")
    input = event['input']
    
    prompt = input.get('prompt')  
    seconds = input.get('seconds', 0)  

    print(f"Received prompt: {prompt}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)  
    
    return prompt 

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler })
