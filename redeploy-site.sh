git fetch && git reset origin/main --hard
source .venv/bin/activate
pip3 install -r requirements.txt # I'm having some issues here
tmux
flask run
