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
    
def adjust_concurrency(current_concurrency):
    max_concurrency = int(os.getenv('MAX_CONCURRENCY', 1))
    return max_concurrency

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler, 'concurrency_modifier': adjust_concurrency})
