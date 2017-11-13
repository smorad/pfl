export PYTHONPATH=$(pwd)
python3 cpos_servers/watchdog.py &
python3 cpos_modes/deployment.py
pkill -f watchdog.py
