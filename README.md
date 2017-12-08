# PFL - Python Flight Layer
### A modular python flight layer for cubesats and smallsats
The purpose of PFL is to enable time and money constrained researchers to write flight software very quickly. This project relies heavily on BSD Stream Sockets, so a flight computer running either Linux or BSD is required.

### Architecture

#### Modes
Modes are what defines your mission. Your modes will run in a state machine, generally your modes will call out to servers to run commands or collect data.

For example, `deployment.py` will command servers to extend an antenna, then send telemetry to ground. After it sends telemetry, it will choose the next phase to be run, in this case that is `detumble.py`.
#### Servers
Servers exist as a translation layer between the hardware and everything else. They send and receive `Msg`s, and can interact with hardware. 

For example, `storage_server.py` will act as a database for storing state (like how many times we've rebooted), as well as binary objects, like photosgraphs. Simply send a `StorageCmd.SAVE` or `StorageCmd.LOAD` via `Msg` to persist or load data.

In `power_server.py`, there should be a way to send a `POWER_LOW` `Msg` to the power server. Once receiving this message, the server should query the power system to see if it is low on power, and respond to the caller.

Servers communicate with the rest of `PFL` via BSD Stream Sockets. This means that you can write a server in any language you choose, as long as it can read and write to sockets.

#### Types
Types exist to make everything a little bit safer. Command types ensure that we don't ask servers to do something that they are
