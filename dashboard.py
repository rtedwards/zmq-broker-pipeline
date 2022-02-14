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
        # ---- USER INPUTS ---- #
        port = st.sidebar.number_input(label="Port:", value=5558)

        # ---- PAGE LAYOUT ---- #
        _, col1, col2, col3, col4, _ = st.columns([1, 2, 1, 1, 1, 1])
        metric_1 = col1.empty()
        metric_2 = col2.empty()
        metric_3 = col3.empty()
        metric_4 = col4.empty()
        metric_1.metric(label="Approx. π", value="n/a")
        metric_2.metric(label="Message Count", value=0)
        metric_3.metric(label="Inside Count", value=0)
        metric_4.metric(label="Outside Count", value=0)

        # col1 displays charts
        # col2 displays live messages comming in with newest at top
        col1, col2 = st.columns([2, 1])
        chart1 = col1.empty()
        data_feed = col2.empty()

        plot = (
            alt.Chart(self.df, height=1000)
            .mark_circle(opacity=1, size=5)
            .encode(x=alt.X("x", axis=None), y=alt.Y("y", axis=None), color=alt.Color("color", legend=None))
        )
        chart1.altair_chart(plot, use_container_width=True)

        # ---- SETUP SOCKET ---- #
        self.setup_socket(port)

        pi = np.nan
        num_inside = 0
        message_count = 0
        df = pd.DataFrame()
        while True:
            prev_pi = pi
            prev_message_count = message_count

            n, x, y, in_circle, language = self.receive_data()

            color = self.colors["red"] if in_circle == 1 else self.colors["blue"]

            message_count += 1
            num_inside += 1 if color == self.colors["red"] else 0
            num_outside = message_count - num_inside

            new_df = pd.DataFrame({"x": [x], "y": [y], "color": [color], "n": [message_count]})
            df = pd.concat([new_df, df])

            pi = 4 * num_inside / message_count

            inside_percent = np.round(num_inside / message_count * 100, 2)
            inside_delta = np.round(inside_percent - (num_inside / message_count * 100), 4)
            outside_percent = np.round(num_outside / message_count * 100, 2)
            outside_delta = np.round(outside_percent - (num_outside / message_count * 100), 4)

            metric_1.metric(label="Approx. π", value=pi, delta=prev_pi - pi)
            metric_2.metric(label="Message Count", value=message_count, delta=prev_message_count - message_count)
            metric_3.metric(label="% Inside", value=f"{inside_percent}%", delta=f"{inside_delta}%")
            metric_4.metric(label="% Outside", value=f"{outside_percent}%", delta=f"{outside_delta}%")

            if message_count % 100 == 0:
                df = df.reset_index(drop=True)
                chart1.add_rows(df)
                data_feed.dataframe(df[["x", "y", "n"]].tail(20), height=1000)
                # df = pd.DataFrame()

    def receive_data(self) -> pd.DataFrame:
        # TODO wrap in method
        msg = self.sink.recv().decode("utf-8")
        msg = str(msg)
        n, x, y, in_circle, language = msg.split(",")
        return (int(n), float(x), float(y), int(in_circle), language)

    def setup_socket(self, port: str):
        self.context = zmq.Context()

        # Socket to receive messages on
        self.sink = self.context.socket(zmq.PULL)
        self.sink.bind(f"tcp://*:{port}")


if __name__ == "__main__":
    SinkPage().display()
