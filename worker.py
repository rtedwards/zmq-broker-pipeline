import zmq

from tools.logging_utils import setup_logger

RECEIVER_PORT = "tcp://localhost:5557"
SENDER_PORT = "tcp://localhost:5558"
CONTROLLER_PORT = "tcp://localhost:5559"

logger = setup_logger(__file__)

language = "python"
context = zmq.Context()

# Socket to receive messages on
logger.info(f"Receiver Port: {RECEIVER_PORT}")
receiver = context.socket(zmq.PULL)
receiver.connect(RECEIVER_PORT)

# Socket to send messages to
logger.info(f"Sener Port: {SENDER_PORT}")
sender = context.socket(zmq.PUSH)
sender.connect(SENDER_PORT)

# Process tasks forever
# TODO context manager for ZMQ ports
while True:
    in_msg = receiver.recv().decode('utf-8')
    in_msg = str(in_msg)
    n, x, y= in_msg.split(",")

    in_circle = 1 if (float(x)**2 + float(y)**2) <= 1 else 0

    msg_string = f"{n},{x},{y},{in_circle},{language}"
    out_msg = msg_string.encode('UTF-8')

    logger.info(f"Message #: {n}")

    sender.send(out_msg)
