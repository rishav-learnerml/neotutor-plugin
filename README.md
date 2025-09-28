# NeoTutor Plugin

NeoTutor Plugin is an advanced AI-powered educational assistant designed to enhance learning experiences by leveraging LLMs and RAG (Retrieval-Augmented Generation) techniques. It provides seamless integration with YouTube transcripts, query enhancement, and polished answer generation for a variety of educational use cases.

## Features

- **LLM Integration:** Utilizes state-of-the-art language models for intelligent responses.
- **RAG Pipeline:** Combines retrieval and generation for context-aware answers.
- **YouTube Transcript Support:** Automatically fetches and processes transcripts for video-based learning.
- **Query Enhancement:** Improves user queries for better results.
- **Polished Answers:** Delivers clear, concise, and well-formatted answers.
- **REST API Endpoints:** Easily interact with the plugin via HTTP requests.
- **Docker Support:** Simple deployment using Docker and Compose.

## Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional, for containerized deployment)

### Installation

#### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rishav-learnerml/neotutor-plugin.git
   cd neotutor-plugin
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

#### Docker Setup

1. Build and run the container:
   ```bash
   docker compose up --build
   ```

## Usage

- Access API endpoints via `http/test_endpoints.http` for testing.
- Integrate with your own applications using the provided REST API.
- Customize LLM and RAG logic in `src/llm/llm.py` and `src/rag/rag.py`.

## Project Structure

```
├── compose.yaml
├── Dockerfile
├── main.py
├── server.py
├── requirements.txt
├── src/
│   ├── llm/
│   ├── rag/
│   ├── schema/
│   └── utils/
├── transcripts/
└── http/
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact [Rishav Chatterjee](mailto:rishavchatterjee@example.com).

---

Enjoy learning with NeoTutor Plugin! 🚀
