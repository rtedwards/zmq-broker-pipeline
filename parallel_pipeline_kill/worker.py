import sys
import time
import zmq

from tools.logging_utils import setup_logger

# TODO: Context manager for ZMQ Ports

RECEIVER_PORT = "tcp://localhost:5557"
SENDER_PORT = "tcp://localhost:5558"
CONTROLLER_PORT = "tcp://localhost:5559"

logger = setup_logger()

context = zmq.Context()

# Socket to receive messages on
logger.info(f"Receiver Port: {RECEIVER_PORT}")
receiver = context.socket(zmq.PULL)
receiver.connect(RECEIVER_PORT)

# Socket to send messages to
logger.info(f"Sener Port: {SENDER_PORT}")
sender = context.socket(zmq.PUSH)
sender.connect(SENDER_PORT)

# Socket for control input
logger.info(f"Controller Port: {CONTROLLER_PORT}")
controller = context.socket(zmq.SUB)
controller.connect(CONTROLLER_PORT)
controller.setsockopt(zmq.SUBSCRIBE, b"")

# Process messages from receiver and controller
poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
poller.register(controller, zmq.POLLIN)

# Process messages from both sockets
while True:
    socks = dict(poller.poll())

    if socks.get(receiver) == zmq.POLLIN:
        message = receiver.recv_string()

        # Process task
        workload = int(message)  # Workload in msecs

        # Do the work
        time.sleep(workload / 1000.0)

        # Send results to sink
        sender.send_string(message)

        # Simple progress indicator for the viewer
        sys.stdout.write(".")
        sys.stdout.flush()

    # Any waiting controller command acts as 'KILL'
    if socks.get(controller) == zmq.POLLIN:
        break

# Finished
receiver.close()
sender.close()
controller.close()
context.term()