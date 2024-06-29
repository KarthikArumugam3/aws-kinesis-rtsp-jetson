import subprocess
import signal
import os

class GStreamerProcess:
    
    def __init__(self, command, shell=True):
        self.command = command
        self.process = None
        self.shell = shell

    def start(self):
        if self.process is not None:
            raise RuntimeError("Process is already running.")
        self.process = subprocess.Popen(self.command, shell=self.shell, preexec_fn=os.setsid)

    def terminate(self, force=False):
        if self.process is None:
            raise RuntimeError("No process is currently running.")
        if force:
            os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
        else:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        self.process.wait()
        self.process = None

    def handle_sigint(self, sig, frame):
        self.terminate()
        print("Streaming stopped due to Keyboard Interrupt")
        exit(0)

    def __enter__(self):
        signal.signal(signal.SIGINT, self.handle_sigint)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.terminate()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
