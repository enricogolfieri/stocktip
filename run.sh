# Create .venv and install requirements if not existt
# enable python virtual environment
# Runs api via streamlit 

#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Virtual environment already exists."
    source .venv/bin/activate
fi

echo "Running Streamlit app..."
streamlit run app.py --server.port 8501 --server.address 0.0.