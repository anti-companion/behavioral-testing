git clone https://github.com/anti-companion/behavioral-testing.git
cd behavioral-testing
git checkout init-proxy-model
cd model-proxy
pip3 install -r requirements.txt
pip3 install -e .
uvicorn main:app --port 9000 --host 0.0.0.0