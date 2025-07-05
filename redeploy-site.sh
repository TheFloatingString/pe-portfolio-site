git fetch && git reset origin/main --hard
source .venv/bin/activate
pip3 install -r requirements.txt # I'm having some issues here
tmux new-session -d -s flask_session 'flask run -host "0.0.0.0"'
tmux attach
