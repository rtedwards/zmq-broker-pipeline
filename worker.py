import sys
import time
import zmq

language = "python"
context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

# Process tasks forever
while True:
    in_msg = receiver.recv().decode('utf-8')
    in_msg = str(in_msg)
    n, x, y= in_msg.split(",")

    in_circle = 1 if (float(x)**2 + float(y)**2) <= 1 else 0

    msg_string = f"{n},{x},{y},{in_circle},{language}"
    out_msg = msg_string.encode('UTF-8')

    # Simple progress indicator for the viewer
    print(f"{n}")

    sender.send(out_msg)
