"""Let you start a slave or master process
"""
import signal
import sys
from actors import Slave, Master

orig_sigint = signal.getsignal(signal.SIGINT)


def run_slave(app_config):
    """Start a slave process

    Parameter:
        app_config (dict): Application configuration
    """
    s = Slave(app_config)

    def terminate(signum, frame):
        signal.signal(signal.SIGINT, orig_sigint)

        try:
            s.stop()
            sys.exit(0)
        except:
            sys.exit(1)

    signal.signal(signal.SIGINT, terminate)
    s.run()


def run_master(app_config):
    """Start the master process

    Parameter:
        app_config (dict): Application configuration
    """
    m = Master(app_config)

    def terminate(signum, frame):
        signal.signal(signal.SIGINT, orig_sigint)

        try:
            m.stop()
            sys.exit(0)
        except:
            sys.exit(1)

    signal.signal(signal.SIGINT, terminate)
    m.run()