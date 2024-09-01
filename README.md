# Customer Support Agent Tutorial Episode 3

In this part of the tutorial we setup langgraph to act as our virtual agent, and gave our agent two tools to ask questions of knowledge bases to:

- Get product reccommendations
- Get business/process information

We designed our agent to act like this:
![Blank diagram (13)](https://github.com/user-attachments/assets/156e98aa-23f2-475d-a167-ac1735a39e79)

So that when we query the chatbot, we can see the retrieved information from the knowledge base and how the chatbot has used the information.


## Setup

To setup the python environment I did:

```bash
conda create -p ./.conda python=3.11
pip install -r requirements.txt
```

Then activated the environment with:
```bash
conda activate ./.conda
```

To run the frontend you can type:

```bash
streamlit run streamlit_frontend.py
```

Happy Agent Building :D"# CustomerSupportAgentEP3" 
