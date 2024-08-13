# Tool for creating RIDDLY decks
This is an admin tool for creating decks and add them to [RIDDLY](https://github.com/GordonShamvey/riddly) mobile app
## How to run
### Using Docker
- Build an image
```bash
docker build -t decks-tool:latest .
``` 
- Run app
```bash
docker run -p 8501:8501 decks-tool:latest
```
- Open app in your browser at http://localhost:8501/
### Using poetry locally
#### Prerequisites: install poetry if you have no with ```pip install poetry```
- Run poetry
```bash
poetry shell
```
- Install deps
```bash
poetry install
```
- Run app
```bash
streamlit run decks_tool/decks_tool.py --server.port=8501 --server.address=0.0.0.0
```
- Open app in your browser at http://localhost:8501/