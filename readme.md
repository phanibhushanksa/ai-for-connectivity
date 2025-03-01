# AIM Network

## Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

2. Install all the required libraries
```bash
pip install -r requirements.txt
```

3. Create an .env file and setup the Groq API key in the .evn file:
```bash
cp .env_template .env
```

4. Run the application with the command:
```bash
streamlit run MAIN.py
```