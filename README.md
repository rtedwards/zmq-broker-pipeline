# zmq-broker-pipeline
Simple example using ZeroMQ as distributed data processing pipeline
![ZMQ Pipeline Approximate Pi](./docs/zmq-pipeline.gif?raw=true "Approximate Pi")

TODO: UML diagram and the ZeroMQ pattern
TODO: artifically slower worker computation

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