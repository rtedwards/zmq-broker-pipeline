from datetime import datetime, timedelta
import time
import random

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import zmq

class LivePage:
    def __init__(self, port: str, topic: str):
        """[summary]

        Args:
            port (str): port to connect to
            topic (str): topic to listen to
        """
        st.set_page_config(
            page_title="Pipeline",
            page_icon="⏳",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # ---- SUBSCRIBER ---- #
        # Socket to talk to server
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)

        self.df = pd.DataFrame(columns=["X", "Y", "color"])
    
    def display(self):

        # ---- USER INPUTS ---- #


        # ---- PAGE LAYOUT ---- #
        # col1 displays charts
        # col2 displays live messages comming in with newest at top
        col1, col2 = st.beta_columns([2, 1])
        approx = col1.empty()
        approx.subheader(f"π ≈ -")
        col2.subheader("Incoming Messages")

        chart1 = col1.empty()
        data_feed = col2.empty()

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x=self.df["X"], y=self.df["Y"], c = self.df["color"], s=2)
        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        ax.set_aspect('equal', 'box')
        chart1.write(fig)
        

        num_in = 0
        num_total = 0
        while True:
            # self.receive_message()
            x = random.uniform(-1,1)
            y = random.uniform(-1,1)
            color = "r" if (x**2 + y**2) <= 1 else "b"
            num_total += 1
            num_in += 1 if color == "r" else 0
            df = pd.DataFrame({"X": [x], "Y": [y], "color": [color]})
            self.df = pd.concat([df, self.df])

            pi = 4 * num_in / num_total

            approx.subheader(f"π ≈ {pi}")
            ax.scatter(x=self.df["X"], y=self.df["Y"], s=2, c=self.df["color"])#, c=colors)
            chart1.write(fig)
            
            # p1 = alt.Chart(df).mark_circle(opacity=1, size=2).encode(
            # alt.X('x1', scale=alt.Scale(domain=(-4, 4))),
            # alt.Y('x2', scale=alt.Scale(domain=(-4, 4))),
            # color=alt.Color('y1', scale=alt.Scale(range=range_)),
            # # facet='facet'
            # )
            # # set some additional properties
            # p1.properties(width=500, height=500, columns=3).resolve_scale()
            # chart1.altair_chart(p1, use_container_width=False)

            # chart1.pyplot(self.data)
            data_feed.write(self.df)
            # time.sleep(0.1)

            
    def receive_message(self) -> pd.DataFrame:
        # TODO wrap in method
            received = self.socket.recv().decode('utf-8')
            topic, msg = received.split(maxsplit=1)
            name, text = msg.split(",")

            new_data = pd.DataFrame({
                "user": [name],
                "comment": [text]
            })
            self.data = pd.concat([new_data, self.data])

if __name__ == "__main__":
    LivePage(port="5555", topic="pi").display()

