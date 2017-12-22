# PFL - Python Flight Layer
### A modular python flight layer for cubesats and smallsats
The purpose of PFL is to enable time and money constrained researchers to write flight software very quickly. This project relies heavily on BSD Stream Sockets, so a flight computer running either Linux or BSD is required.

### Architecture

#### Modes
Modes are what define your mission. Your modes will run in a state machine, generally your modes will call out to servers to run commands or collect data. This should generally be high level and hardware agnostic.

For example, `deployment.py` will command servers to extend an antenna, then send telemetry to ground. After it sends telemetry, it will choose the next phase to be run, in this case that is `detumble.py`.
#### Servers
Servers exist as a translation layer between the hardware and everything else. They send and receive `Msg`s, and can interact with hardware. 

For example, `storage_server.py` will act as a database for storing state (like how many times we've rebooted), as well as binary objects, like photographs. Simply send a `StorageCmd.SAVE` or `StorageCmd.LOAD` via `Msg` to persist or load data.

In `power_server.py`, there should be a way to send a `POWER_LOW` `Msg` to the power server. Once receiving this message, the server should query the power system to see if it is low on power, and respond to the caller.

Servers communicate with the rest of `PFL` via UNIX Stream Sockets. This means that you can write a server in any language you choose, as long as it can read and write to sockets. Simply open up a local socket and read and write to the socket file of the server you'd like to talk to. For now, messages are serialized using Python's `pickle` module. This will likely change to a more general serialization format as servers are written in different languages.

#### Types
Types exist to make everything a little bit safer. Command types ensure that we don't ask servers to do something that they are not expecting. For now, this is a little ugly. This may be replaced with a better RPC mechanism in the future, or at least improved greatly.

### Getting Started
You will need to set your python path to the `src` directory. Do this by exporting the path of this repo: 
```
$ cd pfl/src
$ export PYTHONPATH="$(pwd)"
```
Once you've done that, you should be able to test everything by running
`$ src/bootstrap.sh` from the `src` directory. This will spawn the watchdog, the servers, and run through a few phases. This is used to test each phase you've written individually. If you'd like to test the full flow using the state machine, go ahead and run 
```
# Spawn subsystem servers for the state machine to talk to
$ src/pfl_servers/watchdog.py
# Spawn the state machine and run through the states
$ src/pfl_modes/state_machine.py```

