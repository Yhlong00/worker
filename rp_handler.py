import runpod
import os
import time

# load models

def adjust_concurrency(max_concurrency):
    max_concurrency = int(os.environ.get('MAX_CONCURRENCY', '1')) 
    
    print(f"Max Concurrency: {max_concurrency}")  

    return max_concurrency 

def handler(event):
    """RunPod job handler that runs the WebSocket server and waits for shutdown."""
    input = event['input']
    
    prompt = input.get('prompt', 'Hello World')  
    seconds = input.get('seconds', 0)  
    
    time.sleep(seconds)  
    # Start WebSocket server and wait for shutdown message
    return prompt

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler,  "concurrency_modifier": adjust_concurrency})
