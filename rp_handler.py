import runpod
import os
import time

# load models
# hihi

def adjust_concurrency(max_concurrency):
    max_concurrency = int(os.environ.get('MAX_CONCURRENCY', '1')) 
    
    print(f"Max Concurrency: {max_concurrency}")  

    return max_concurrency 

# Basic:
# def handler(event):
#     """RunPod job handler that runs the WebSocket server and waits for shutdown."""
#     input = event['input']
    
#     prompt = input.get('prompt', 'Hello World')  
#     seconds = input.get('seconds', 0)  
    
#     time.sleep(seconds)  
#     # Start WebSocket server and wait for shutdown message
#     return prompt

# Stream:
def handler(event):
    input = event['input']
    text = input.get('text', "Hello from Runpod!")
    delay = input.get('delay', 2)

    print(f"Processing text: {text}")

    # Stream character by character
    for char in text:
        time.sleep(delay)
        yield {"status": "processing", "chunk": char}

    yield {"status": "completed", "message": "Character streaming completed"}


if __name__ == '__main__':
    runpod.serverless.start({'handler': handler,  "concurrency_modifier": adjust_concurrency})
