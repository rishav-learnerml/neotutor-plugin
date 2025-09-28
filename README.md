<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/MCP%20Enabled-yes-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-ready-blue?style=for-the-badge" />
</p>

<h1 align="center">🚀 NeoTutor Plugin</h1>

<p align="center">
  <b>Supercharge your learning with AI, RAG, and Model Context Protocol (MCP)!</b>
</p>

NeoTutor Plugin is a next-gen educational assistant that leverages LLMs, RAG (Retrieval-Augmented Generation), and MCP (Model Context Protocol) for smarter, context-aware answers. Seamlessly integrates with YouTube transcripts, enhances queries, and delivers polished, actionable responses for students, educators, and lifelong learners.

## ✨ Features

- **LLM Integration:** State-of-the-art language models for intelligent, adaptive responses.
- **RAG Pipeline:** Combines retrieval and generation for context-rich answers.
- **MCP Support:** Out-of-the-box Model Context Protocol (see `server.py`) for advanced model orchestration and plugin interoperability.
- **YouTube Transcript Support:** Fetch and process transcripts for video-based learning.
- **Query Enhancement:** AI-powered query improvement for better results.
- **Polished Answers:** Clear, concise, and well-formatted responses.
- **REST API Endpoints:** Interact via HTTP requests or MCP.
- **Docker & Compose:** Effortless deployment and scaling.

## 🚦 Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)

### Installation

#### Local Setup

```zsh
# Clone the repo
$ git clone https://github.com/rishav-learnerml/neotutor-plugin.git
$ cd neotutor-plugin

# Install dependencies
$ pip install -r requirements.txt

# Run the FastAPI server
$ python server.py
```

#### Docker Setup

```zsh
# Build and run with Docker Compose
$ docker compose up --build
```

#### MCP Mode

```zsh
# Run with Model Context Protocol (MCP)
$ python server.py   # (for FastAPI)
$ python server.py   # (for MCP)
# Or use: python server.py --mcp
```

## 🛠️ Usage

- Test API endpoints via [`http/test_endpoints.http`](http/test_endpoints.http).
- Integrate with your apps using REST or MCP.
- Customize LLM and RAG logic in [`src/llm/llm.py`](src/llm/llm.py) and [`src/rag/rag.py`](src/rag/rag.py).
- MCP entrypoint: see [`server.py`](server.py) for FastMCP integration.

## 📁 Project Structure

```text
├── compose.yaml         # Docker Compose config
├── Dockerfile           # Container build file
├── main.py              # FastAPI app
├── server.py            # MCP entrypoint
├── requirements.txt     # Python dependencies
├── src/
│   ├── llm/             # LLM logic
│   ├── rag/             # RAG pipeline
│   ├── schema/          # Query schemas
│   └── utils/           # Utility functions
├── transcripts/         # Saved transcripts
└── http/                # HTTP endpoint tests
```

## 🤝 Contributing

We welcome contributions! Open issues, submit pull requests, or suggest features to make NeoTutor even better.

## 📜 License

MIT License. See [`LICENSE`](LICENSE) for details.

## 📬 Contact

Questions or support? Reach out to [Rishav Chatterjee](mailto:rishavchatterjee@example.com).

---

<p align="center">
  <b>Enjoy learning with NeoTutor Plugin!</b> <br>
  <img src="https://img.shields.io/badge/Powered%20by%20FastAPI-005571?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/Model%20Context%20Protocol-MCP-blue?style=flat-square" />
  <br>
  <img src="https://img.shields.io/badge/LLM%20%26%20RAG%20Inside-ff69b4?style=flat-square" />
  <br>
  <img src="https://img.shields.io/badge/NeoTutor%20Plugin-🚀-yellow?style=flat-square" />
</p>
