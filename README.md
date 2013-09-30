WebMPC
======

RESTful client and web interface for Music Player Daemon.

The server part is written in Python using CherryPy, so you'll need to install it (normally it comes as a standard Python module).
The client part uses jQuery, and it carries a snapshot, so you won't need Internet access to run it.

**Currently it's not even close to release, so be prepared to do some manual work like editing host/port in the source code.**

Running
-------

1.  Edit config.py providing your hosts and ports.
2.  Run ./webmpc.py
