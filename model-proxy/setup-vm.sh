git clone https://github.com/anti-companion/behavioral-testing.git
git checkout init-model-proxy
cd behavioral-testing
cd model-proxy
pip3 install -r requirements.txt
pip uninstall nvidia_cublas_cu11 -y
pip3 install -e .
MODEL_NAME=PygmalionAI/pygmalion-350m uvicorn main:app --port 9000 --host 0.0.0.0