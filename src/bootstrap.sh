export PYTHONPATH=$(pwd)
print $0
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
find $ROOT_DIR -name *.checksum -delete
python3 cpos_servers/watchdog.py &
python3 cpos_modes/deployment.py
# Reap children
pkill -P $$
