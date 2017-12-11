export PYTHONPATH=$(pwd)
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Clear old checksums 
# TODO: remove before launch
find $ROOT_DIR -name *.checksum -delete
# Get rid of sockets left open from pkill
# so our debug messages aren't polluted
find /tmp/ -type s | grep -v tmux | xargs rm || true

# Create our /mode socket subdir
mkdir -p /tmp/mode
echo
echo 'Watchdog Init:'
echo '---------------------------------'
python3 pfl_servers/watchdog.py &
# Keep watchdog init logs out of the deployment segment
sleep 1
echo '---------------------------------'
echo

echo 'Deployment Phase:'
echo '---------------------------------'
python3 pfl_modes/deployment.py
echo '---------------------------------'
echo

echo 'Detumble Phase:'
echo '---------------------------------'
python3 pfl_modes/detumble.py
echo '---------------------------------'
echo

echo 'SafeMode Phase:'
echo '---------------------------------'
python3 pfl_modes/safe_mode.py
echo '---------------------------------'

# Reap children
echo '---------------------------------'
echo 'Test complete, terminating...'
pkill -P $$
echo '---------------------------------'
