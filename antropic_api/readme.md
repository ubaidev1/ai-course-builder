# AI-Powered Course Content Generator

This project extracts course content from a PDF and generates a JSON structure using AI. The AI uses a prompt to create a structured course with modules, lessons, and quizzes based on the content in the PDF file.

## Prerequisites

Before running the code, ensure that you have the following Python libraries installed. You can install them using `pip`:

```bash
pip install PyPDF2
pip install anthropic
```

### Required Libraries:

- **PyPDF2**: This library is used to extract text from PDF files.
- **anthropic**: This is a client library used to communicate with the Anthropic Claude AI API.

## Project Structure

- **`config.json`**: This file stores configuration variables like the API key, AI model, prompt template, and other parameters.
- **`anthropic_response.py`**: This is the main Python file that processes the PDF and communicates with the AI to generate the course content JSON.
  
Make sure that both `config.json` and `anthropic_response.py` are in the **same directory** so that the code can correctly read the configuration file.

## Usage Instructions

The function that backend team needs to use is:

### `get_ai_course_details(config_file, pdf_file_path)`

This function reads the configuration from `config.json` and extracts course details from the provided PDF file, returning a structured JSON output.

### Parameters:
1. **`config_file` (str)**: The path to the `config.json` file, which contains the API key and prompt template.
2. **`pdf_file_path` (str)**: The path to the PDF file from which the content will be extracted.

### Example Usage:

```python
json_output = get_ai_course_details('config.json', 'test.pdf')
print(json_output)
```

## Important Notes:

- The backend only needs to call the `get_ai_course_details` function, passing the configuration file path and the PDF file path as arguments.
- The `config.json` file should contain a valid API key for accessing the Anthropic Claude AI model.

---