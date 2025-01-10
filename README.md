# Shard - Open Source Video Understanding API and Large Vision Model Observability Platform.

Shard is an open-source library designed to provide observability and video understanding capabilities for Large Vision Models (LVMs) like OpenAI's Sora. It helps developers monitor, analyze, and understand the behavior and performance of vision models in production.

## Features

- LVM Performance Monitoring
- Video Understanding API
- Model Behavior Analysis
- Integration with Popular Vision Models
- Observability Metrics and Dashboards

## Installation and Development Setup

1. Clone the repository:

```bash
git clone https://github.com/Shard-AI/Shard.git
cd Shard
```

2. Configure your virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Copy the environment variables file:

```bash
cp .env.example .env

```

4. Set up your API keys in the .env file:

```
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_HOSTNAME=localhost
REDIS_PORT=6379
```

5. Export the environment variables:

```bash
source export_env.sh
```

6. Run the API Server:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

7. Run the Asynchronous Worker:

```bash
celery -A src.core.async_worker worker --loglevel=info --pool=threads
```

## Quick Start

```python
from axos import VideoAnalyzer

# Initialize the analyzer
analyzer = VideoAnalyzer()

# Analyze a video
results = analyzer.analyze("path/to/video.mp4")
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [docs.shard.video](https://docs.shard.video)
- Issue Tracker: [GitHub Issues](https://github.com/Shard-AI/Shard/issues)
- Contact: [founders@shard.video](mailto:founders@shard.video)
<!-- - Discord Community: [Link to Discord](https://discord.gg/shard) -->
