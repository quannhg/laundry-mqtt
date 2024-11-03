# laundry-mqtt
## Pre-requisites
- To create new account, add password and username in `mosquitto/config/passwd` file
## How to run
1. Start the container
```bash
docker-compose up -d
```
### How to test
There is a python to test.
1. Enter environment
```bash
source venv/bin/activate
```
2. Install dependencies in requirements.txt
```bash
pip install -r requirements.txt
```
3. Run the test
```bash
python test.py
```
Enter message id to test specific message, use can add more id if needed
