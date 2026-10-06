
from python:3.11-slim 

WORKDIR /app

copy requirements.txt .

Run  pip install -r requirements.txt

copy . .

expose 5000

cmd ['python','ui.py']


