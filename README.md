
# AI Image Recognition with OpenAI GPT API

This project leverages the OpenAI GPT API to analyze images and detect objects based on a given search term. The script can recognize objects within an image and trigger actions based on the recognition, such as running a command.

## Features

- **Object Detection:** Use a search term to query if a specific object or set of objects is present in an image.
- **Customizable Action Trigger:** Trigger a custom command when the object is detected (e.g., run a script, send an email).
- **Logging:** Logs the image analysis results and the entire prompt for traceability.
- **Fast Processing:** Efficiently analyzes images with minimal processing time.

## Requirements

- Python 3.x
- `requests` library for API calls
- OpenAI API key (set as environment variable: `OPENAI_API_KEY`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/xdrfvgz/ai-image-recognition.git
   cd ai-image-recognition
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the script with the following command:

```bash
python recog.py <image_path> <search_term> <command_to_run_on_detection>
```

### Example:

```bash
python recog.py /path/to/image.jpg "Mensch" "bash alarm.sh"
```

- `<image_path>`: The path to the image file you want to analyze.
- `<search_term>`: The object you're searching for in the image.
- `<command_to_run_on_detection>`: The command to run if the object is detected (e.g., play a sound, send an alert).

## Logging

All search queries and results are logged in `log.txt`. The log contains the image path, search term, the result of the query (e.g., `ALARM` or `SAFE`), and the full prompt that was sent to the API.

## Example Log Entry

```
/path/to/image.jpg: Suchbegriff -> Mensch, Ergebnis -> ALARM, Prompt -> Zu suchende(s) Objekt(e): Mensch; Wenn du alle gesuchten Objekte nach exakt der Beschreibung siehst, schreibst du [ALARM], ansonsten [SAFE].
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
