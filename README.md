# Python Programming Project 'Stock Market Technical Analyzer'

### Dependencies 
```

Python v3.12.0+ 
Bootstrap v5.2.3 [Front-end library]
conda 24.5.0 [Virtual Environment]

```
requirements.txt (Pip packages)

These are the main-packages required.
```
# Main Packages for the Web App
Flask==3.0.3
setuptools==74.1.2 
# Environment variable handling
python-dotenv== 1.0.1
# yfinance API
yfinance==0.2.43
# Analysis
numpy==1.26.4 # Force Numpy to use 1.26.4 for pandas_ta comptability
pandas_ta== 0.3.14b0
scikit-learn==1.5.2
# Visualisation
matplotlib==3.9.2
plotly==5.22.0
# Login System, Persistent Storage for Portfolio data etc
Flask-Login==0.6.3
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
Werkzeug==3.0.4
WTForms==3.1.2
# Jupyter notebook related packages to develop with inside vscode
jupyter
jupyter_client
jupyter_core 
notebook 
ipykernel
ipython
nbformat==5.10.4
nbconvert
traitlets
stack_data
```
### VS Code Extensions used in development
Download these extension for this project.
```
Python (ms-python.python)
Pylance (ms-python.vscode-pylance)
Jupyter (ms-toolsai.jupyter)
Jupyter Keymap (ms-toolsai.jupyter-keymap)
Jupyter Renderers (ms-toolsai.jupyter-renderers)
Jupyter Cell Tags (ms-toolsai.vscode-jupyter-cell-tags)
Jupyter Slideshow (ms-toolsai.vscode-jupyter-slideshow)
```

### Instruction
1. Clone repository in github desktop, create a new branch based on 'development', do your work in that branch
2. Install Conda Environment if haven't done so and activate it
3. Install the python packages
4. Create .env file in root dir
---

1. Clone GitHub Repo

2. Install Conda Environment
```
Download anaconda package manager
https://www.anaconda.com/download

```
3. Python Packages Installation
```
pip install -r requirements.txt  
```

Packages Reinstallation
```
pip freeze > uninstall.txt    # Writes currently installed packages to list
pip uninstall -r uninstall.txt -y #Base on the list uninstall all installed packages
pip install -r requirements.txt   # Reinstall if needed
```

4.Create .env file in the root directory (same dir as the run.py, README.md files) 
```
```
