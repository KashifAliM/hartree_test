# Hartree.Test project

### How to setup the virtual environment 

```bash
# Create the environment
python -m venv .venv

# Activate the environment
.venv/Scripts/activate

#install the requirement
pip install requirements.txt

# Run the program
python src/using_pandas.py


```


### Running the program (Docker)

```bash
1. docker build -t hartreetestapp .

2. docker run -it --name hartreetestapp hartreetestapp:latest /bin/bash

3. python src/using_pandas.py

```