
# Screenshot Text Extractor & Conversational AI Assistant

## Overview
This Python-based application combines Optical Character Recognition (OCR) with a conversational AI assistant, designed to enhance productivity and streamline workflows. The program automatically detects screenshots, extracts text, and interacts with the user by explaining the text and generating relevant questions. Additionally, users can engage in dynamic chat-based conversations with the AI. The program runs efficiently in the background, with a user-friendly interface for seamless interaction.

## Features
- **Automatic Text Extraction**: Captures and extracts text from screenshots in real-time using Tesseract OCR.
- **AI-Powered Explanations**: The extracted text is automatically sent to an AI model (via Ollama API), which provides detailed explanations.
- **Interactive Chat Interface**: Users can engage with the AI through a chat interface that supports conversational inputs and generates intelligent responses.
- **System Tray Integration**: The app minimizes to the system tray, allowing it to run unobtrusively in the background.
- **Customizable UI**: Built with the CustomTkinter framework for a modern and sleek interface, offering system-level appearance themes.

## Key Components
- **Tesseract OCR**: Integrated with Tesseract for accurate text extraction from images or screenshots.
- **Ollama API**: Utilizes the Mistral model to handle dynamic, context-aware conversations, generating responses based on user input and extracted text.
- **Tkinter & CustomTkinter**: Provides a smooth, modern graphical user interface (GUI), offering a polished user experience.
- **Pystray Integration**: Allows the program to minimize to the system tray, making it easily accessible without cluttering the desktop.
- **Multithreaded Processing**: Runs text extraction and AI response generation in the background without interrupting the user experience.

## How It Works
1. **Screenshot Detection**: The program monitors the clipboard for screenshots.
2. **Text Extraction**: Once a screenshot is detected, the program extracts the text using Tesseract OCR.
3. **AI Interaction**: The extracted text is automatically sent to the AI, which provides explanations and optionally generates relevant questions.
4. **User Chat**: Users can also manually chat with the AI via a clean and intuitive chat interface, allowing for real-time interaction.
5. **Tray Integration**: The app runs in the background and can be accessed from the system tray at any time.

## Installation & Setup
1. Install the required dependencies:
   ```bash
   pip install pytesseract Pillow pystray customtkinter ollama
   ```
2. Ensure Tesseract-OCR is installed on your system. Set the correct path to the Tesseract executable in the script:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Future Enhancements
- **Automated Question Generation**: Expand the AI’s capabilities to automatically generate more complex, multi-faceted questions based on extracted text.
- **Additional Language Support**: Extend the OCR and AI capabilities to handle multiple languages.

## License
This project is open-source and available under the MIT License.
