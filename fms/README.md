Steps for running FMS chatbot on AMD dev box

Ollama is already running on AMD; as long as you do not change the OLLAMA_CHAT_MODEL in fms/chatbot.py, the model is already pulled and you do not need to do any Ollama setup.

1. Configure your environment

module load miniforge
conda create -n msdagents python=3.12 pip
conda activate msdagents
pip install -e .

2. Create the Database

First, you need to have Milvus started:

cd MSDAgents
mkdir -p $(pwd)/volumes/milvus
./start_milvus_service.sh

Then, you can create the database:

cd fms
python create_fms_database.py

3. Last Step: Run the Chatbot

python chatbot.py
