# Network Traffic Analyzer — Demo

A walkthrough of live capture and analysis. Screenshots are in the `assets/` folder.

## Python

```bash
cd python && uv sync
sudo netanal capture -i eth0
```

## C++

```bash
cd cpp && ./install.sh
just run -i eth0
```

## Live capture and analysis

The capture view shows real-time packet logging, a capture summary, protocol distribution breakdown, and top talkers ranked by bytes.

![Capture](assets/capture.png)
