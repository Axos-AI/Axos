# Shard - Open Source Video Understanding API and Large Vision Model Observability Platform.

Shard is an open-source library designed to provide observability and video understanding capabilities for Large Vision Models (LVMs) like OpenAI's Sora. It helps developers monitor, analyze, and understand the behavior and performance of vision models in production.

## Features

- LVM Performance Monitoring
- Video Understanding API
- Model Behavior Analysis
- Integration with Popular Vision Models
- Observability Metrics and Dashboards

## Quick Start

```python
from src.sdk import Shard

# Initialize the client
client = Shard("your_api_key_here")

# Interpret a video
response = client.interpret("/absolute/path/to/video.mp4")

# Analyze prompt adherence
analysis = client.gauge_prompt_adherance("/absolute/path/to/video.mp4", "your prompt here")
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Shard-AI/Shard.git
cd Shard
```

2. Set up your environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
source export_env.sh
```

6. Run the API (in two terminals):

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
celery -A src.core.async_worker worker --loglevel=info --pool=threads
```

## Documentation

Visit our [documentation](https://docs.shard.video) for detailed guides and API reference.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

Contact us at [founders@shard.video](mailto:founders@shard.video)
