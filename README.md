# AI-Driven Academic Writing Agent

An intelligent system for automating the generation of state-of-the-art (SOTA) academic reviews using LangChain and Together AI's LLMs.

## Features

- PDF and research paper link processing
- Automated content extraction and synthesis
- Citation management and formatting
- Multiple output formats (LaTeX, Markdown, DOCX, PDF)
- Customizable review generation
- Academic writing style compliance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abbasmsh1/researcher.git
cd researcher
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

## Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Access the web interface at `http://localhost:8000`

3. API endpoints:
- POST `/api/process-paper`: Submit a paper for processing
- POST `/api/generate-review`: Generate a review from processed papers
- GET `/api/citations/{style}`: Get formatted citations

## Project Structure

```
researcher/
├── app/
│   ├── api/            # API routes
│   ├── core/           # Core business logic
│   ├── models/         # Data models
│   ├── services/       # External services integration
│   └── utils/          # Utility functions
├── tests/              # Test cases
├── frontend/           # React.js frontend
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Configuration

The system can be configured through environment variables:

- `TOGETHER_API_KEY`: Together AI API key
- `MONGODB_URI`: MongoDB connection string
- `POSTGRES_URI`: PostgreSQL connection string
- `MAX_PAPERS`: Maximum number of papers to process simultaneously
- `OUTPUT_FORMATS`: Enabled output formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details.

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{researcher2024,
  title={AI-Driven Academic Writing Agent},
  author={Abbas Mustafa},
  year={2025},
  url={https://github.com/abbasmsh1/researcher}
}
``` 