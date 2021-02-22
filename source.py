import random
import time

import numpy as np
import pandas as pd
import streamlit as st
import zmq

class SourcePage:

    def __init__(self):

        # Initialize random number generator
        random.seed()

        self.n = 0
        self.context: zmq.sugar.context.Context
        self.vent: zmq.sugar.socket.Socket

    def display(self):

        st.title("Ventillator")

        # ---- USER INPUTS ---- #
        port = st.sidebar.number_input(label="Port:", value=5557)
        n_points = st.sidebar.number_input(label="N points:", min_value=0, value=1000)
        button = st.sidebar.empty()

        # ---- SETUP SOCKET ---- #
        self.setup_socket(port)

        # ---- PROCESS ---- #
        x = np.random.uniform(-1,1, n_points)
        y = np.random.uniform(-1,1, n_points)
        data = np.array([x, y]).T

        # ---- SEND DATA ---- #
        if button.button(label="Send Data"):
            with st.spinner("Sending data..."):
                try:
                    self.send_data(data)
                except KeyboardInterrupt as k:
                    st.info(k)
                finally:
                    # clean up
                    self.vent.close()
                    self.context.term()
                    pass

    def send_data(self, data):
        bar = st.progress(0)
        total = len(data)
        for i, d in enumerate(data):
            self.n += 1
            msg_string = f"{self.n},{d[0]},{d[1]}"
            msg_bytes = msg_string.encode('UTF-8')

            self.vent.send(msg_bytes)
            bar.progress(i / total)
        
    def setup_socket(self, port: str):
        # try:
        #     self.vent.close()
        #     self.context.term()
        # except Exception as e:
        #     # st.sidebar.info("Sockets closed")
        #     # st.write(e)
        #     pass

        self.context = zmq.Context()

        # Socket to send messages on
        self.vent = self.context.socket(zmq.PUSH)
        self.vent.bind(f"tcp://*:{port}")

if __name__ == "__main__":
    SourcePage().display()