import json
import re

import PyPDF2
import anthropic


# Functional Style Setup
def load_config(config_file):
    """Load configuration variables from a JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)


def initialize_client(api_key):
    """Initialize the Claude client with the API key."""
    return anthropic.Anthropic(api_key=api_key)


def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF file."""

    def read_page_text(file):
        reader = PyPDF2.PdfReader(file)
        return ''.join([page.extract_text() for page in reader.pages])

    with open(pdf_path, 'rb') as file:
        return read_page_text(file)


def create_prompt_from_template(pdf_text, prompt_template):
    """Combine the prompt template with the PDF content."""
    return f"""
                   Here is the content of the PDF:
                   <pdf_content>
                   {pdf_text}
                   </pdf_content>
                   {prompt_template}
               """



def send_prompt_to_claude(client, prompt, model, max_tokens, temperature, system):
    """Send the prompt to the Claude API and get a response."""
    return client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )


def extract_json_from_message(message_content):
    """
    Extract and parse JSON from the Claude message response.
    """
    message_text = ''.join(block.text for block in message_content.content)
    json_match = re.search(r'{.*}', message_text, re.DOTALL)

    if json_match:
        json_string = json_match.group(0).strip()
        return parse_json(json_string)
    return "No JSON found in the message."


def parse_json(json_string):
    """Parses JSON string and returns formatted JSON or an error message."""
    try:
        json_object = json.loads(json_string)
        return json.dumps(json_object, indent=4)
    except json.JSONDecodeError as e:
        error_context = json_string[e.pos - 50:e.pos + 50]
        return f"Invalid JSON format: {e.msg} at line {e.lineno} column {e.colno}\nContext: {error_context}"


def get_ai_course_details(config_file, pdf_file_path):
    """Main function to orchestrate the PDF to JSON extraction."""
    # Load configuration
    config = load_config(config_file)

    # Initialize client
    client = initialize_client(config['API_KEY'])

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # Create the prompt using the template
    prompt = create_prompt_from_template(pdf_text, config['prompt_template'])

    # Send the prompt to Claude
    message = send_prompt_to_claude(
        client,
        prompt,
        config['model'],
        config['max_tokens'],
        config['temperature'],
        config['system']
    )

    # Extract and parse the JSON from Claude's response
    return extract_json_from_message(message)

# Run the main function
# if __name__ == "__main__":
#     config_file = "config.json"  # The JSON file with the configuration
#     pdf_file_path = "test.pdf"  # Path to your PDF file
#
#     json_output = get_ai_course_details(config_file, pdf_file_path)
#     print(json_output)
