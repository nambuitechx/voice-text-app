# Voice Text Application

### Run with docker
Not recommend to run on Docker because currently we need to download model to local to run the STT and TTS,
which leads to the size of the image is too large.


### Run without docker
#### Backend
1. On root of project, run `cd backend`
2. If do not have the installed virtual environment yet:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Run `python main.py`

#### Frontend
1. On root of project, run `cd frontend`
2. Run `npm install`
3. Run `npm run dev`
