# Just testing threading availability on device
import threading
import random
import time

def viewer(channel : int, value : int):
    print(f"Channel : {channel}\tViewer getting value : {value}")

def streamer(channel : int):
    x = random.randint(1,100)
    print(f"Channel : {channel}\tStreamer sending value : {x}")
    return x

def channel(x : int):
    print(f"Initiailized channel number : {channel}")
    for i in range(100):
        c = streamer(x)
        # time.sleep(0.001)
        viewer(x, c)

if __name__ == "__main__":
    v = threading.Thread(target=channel, args=(1,))
    print("Starting the streaming client")
    v.start()
    print("Waiting for shit to finish")
    v.join()
    print("All done")
