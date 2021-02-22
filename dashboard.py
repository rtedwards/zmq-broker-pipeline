from datetime import datetime, timedelta
import time
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import zmq

class SinkPage:
    def __init__(self):
        """[summary]

        Args:
            port (str): port to connect to
            topic (str): topic to listen to
        """
        self.colors = {"blue": "#5276A7", "green": "#57A44C", "red": "#8B0000"}

        st.set_page_config(
            page_title="Pipeline",
            page_icon="⏳",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        self.df = pd.DataFrame({"x": [0.0], "y": [0.0], "color": ["#8B0000"], "n": [0]})
    
        self.context: zmq.sugar.context.Context
        self.sink: zmq.sugar.socket.Socket
        
    def display(self):
        st.title("Sink")
        # ---- USER INPUTS ---- #
        port = st.sidebar.number_input(label="Port:", value=5558)

        # ---- PAGE LAYOUT ---- #
        # col1 displays charts
        # col2 displays live messages comming in with newest at top
        col1, col2 = st.beta_columns([2, 1])
        approx = col1.empty()
        num_messages = col2.empty()
        approx.subheader(f"π ≈ -")
        num_messages.subheader(f"Messages: ")

        chart1 = col1.empty()
        data_feed = col2.empty()

        plot = alt.Chart(self.df, height=500, width=500).mark_circle(opacity=1, size=5).encode(
                x=alt.X('x', axis=None),
                y=alt.Y('y', axis=None),
                color=alt.Color('color', legend=None)
            )
        chart1.altair_chart(plot)

        # ---- SETUP SOCKET ---- #
        self.setup_socket(port)

        num_in = 0
        num_total = 0
        while True:
            n, x, y, in_circle, language = self.receive_data()

            color = self.colors["red"] if in_circle == 1 else self.colors["blue"] 
            num_total += 1
            num_in += 1 if color == self.colors["red"] else 0
            df = pd.DataFrame({"x": [x], "y": [y], "color": [color], "n": [num_total]})
            self.df = pd.concat([df, self.df])
            self.df.set_index("n")

            pi = 4 * num_in / num_total

            approx.subheader(f"π ≈ {pi}")
            num_messages.subheader(f"Messages: {num_total}")
            chart1.add_rows(df)
            
            # data_feed.write(self.df)

            
    def receive_data(self) -> pd.DataFrame:
        # TODO wrap in method
        msg = self.sink.recv().decode('utf-8')
        msg = str(msg)
        n, x, y, in_circle, language = msg.split(",")
        return ( int(n), float(x), float(y), int(in_circle), language )

    def setup_socket(self, port: str):
        self.context = zmq.Context()

        # Socket to receive messages on
        self.sink = self.context.socket(zmq.PULL)
        self.sink.bind(f"tcp://*:{port}")

if __name__ == "__main__":
    SinkPage().display()

