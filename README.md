# zmq-broker-pipeline
Simple example of using ZeroMQ as distributed data processing pipeline to approximate π.  
Points are randomly generated between [-1, 1] in x and y axes.  The number of points that fall within the unit circle
over the number of points that fall outside the unit circle approachs π as the limit -> ∞.
![ZMQ Pipeline Approximate Pi](./docs/zmq-pipeline.gif?raw=true "Approximate Pi")

## Dependencies
```bash
conda create -n pipeline python=3.9
conda activate pipeline

pip install pip-compile-multi
pip-compile-multi

pip install -e .
```

## Setup Workers
Startup as many workers as needed via
```bash
python worker.py
```

## Setup Sink
```bash
streamlit run dashboard.py
```

## Setup Source
```bash
streamlit run source.py
```

## Running
Once the dashboard and workers are spun up one can start streaming data from the source dashboard.

## TODO
- UML diagram and the ZeroMQ pattern
- artifically slower worker computation