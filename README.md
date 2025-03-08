# Academic Research Assistant

A powerful research assistant built with LangChain and TogetherAI's Deepseek model that helps with academic paper analysis, generation, and summarization.

## Features

- Upload and process academic papers (PDF, DOCX, TXT formats)
- Generate IEEE-style research papers based on uploaded references
- Summarize academic papers for quick understanding
- Modern web interface with real-time feedback

## Prerequisites

- Python 3.8 or higher
- TogetherAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd researcher
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your TogetherAI API key:
```
TOGETHER_API_KEY=your_api_key_here
MODEL_NAME=deepseek-ai/deepseek-coder-33b-instruct
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:
```bash
python run.py
```
3. Open your web browser and navigate to `http://localhost:5000`

## Usage

### Uploading Reference Papers
1. Click on "Choose Files" in the Upload Reference Papers section
2. Select one or more academic papers (PDF, DOCX, or TXT format)
3. Click "Upload Papers" to process them

### Generating a Paper
1. Enter your research topic
2. Add relevant keywords (comma-separated)
3. Specify focus points (comma-separated)
4. Click "Generate Paper"
5. The generated paper will appear in the Results section

### Summarizing a Paper
1. Select a paper to summarize
2. Click "Summarize Paper"
3. The summary will appear in the Results section

## Notes

- The application uses FAISS for efficient vector storage and retrieval
- Papers are processed and stored in chunks for better context management
- All uploaded files are temporarily stored and automatically cleaned up after processing
- The generated papers follow IEEE formatting guidelines
- Summaries include main objectives, key findings, methodology, and conclusions

## Security Considerations

- API keys should be kept secure and never committed to version control
- The application includes file type validation and size limits
- Uploaded files are processed and removed immediately after use

## License

MIT License 