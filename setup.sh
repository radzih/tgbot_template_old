echo "Creating venv..."
python -m venv env 
echo "Activating venv..."
. env/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
