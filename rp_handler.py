import runpod
import time  

def handler(event):
    input = event['input']
    
    instruction = input.get('instruction')  
    seconds = input.get('seconds', 0)  

    print(f"Received instruction: {instruction}")
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)  
    result = instruction.replace(instruction.split()[0], 'created', 1)
    print(f"Modified instruction: {result}")
    
    return result 

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
