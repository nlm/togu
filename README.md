togu
====

Health check for shinken daemons running under supervisor

description
-----------

Togu is a small service which will periodically 'ping' a shinken daemon via its http api interface to check if the daemon is alive and responding. If it's not, it triggers a restart of the designated service via the supervisor rpc interface.

As it uses supervisor eventlistener interface and triggers restarts via supervisor rpc,
It must be started as an `[eventlistener]`, and shinken services must be run as `[program]`, both under supervisor.

(by the way, it's a good thing to have shinken daemons babysitted by a process supervisor like *supervisor*, *runit*, *daemontools* or *upstart*, etc.)

example supervisor config:

    [program:shinken-poller]
    command = /usr/bin/shinken-poller -c /etc/shinken/daemons/pollerd.ini
    user = shinken
    autostart = true
    autorestart = true
    stopasgroup = true
    stderr_logfile = /dev/null
    stdout_logfile = /dev/null

    [eventlistener:togu-poller]
    command = togu -n shinken-poller -p 7771
    events = TICK_5
    user=togu
    stdout_logfile = /dev/null
    stderr_logfile = /var/log/supervisor/%(program_name)s.log

usage
-----

    usage: togu [-h] --port PORT --service-name SERVICE [--retry TIMES]
                [--timeout SECONDS]

    -h, --help            show this help message and exit
    
    --port PORT, -p PORT  port of the shinken daemon to check
    
    --service-name SERVICE, -n SERVICE
                          name of the service in supervisord
    
    --retry TIMES, -r TIMES
                          number of times to retry before restarting
    
    --timeout SECONDS, -t SECONDS
                          maximum time to respond to ping probes

install
-------

Togu is available via pip

    pip install togu
