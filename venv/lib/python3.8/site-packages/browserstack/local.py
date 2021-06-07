import subprocess, os, time, json, psutil
from browserstack.local_binary import LocalBinary
from browserstack.bserrors import BrowserStackLocalError

class Local:
  def __init__(self, key=None, binary_path=None):
    self.key = os.environ['BROWSERSTACK_ACCESS_KEY'] if 'BROWSERSTACK_ACCESS_KEY' in os.environ else key
    self.options = None
    self.local_logfile_path = os.path.join(os.getcwd(), 'local.log')

  def __xstr(self, key, value):
    if key is None:
      return ['']
    if str(value).lower() == "true":
      return ['-' + key]
    else:
      return ['-' + key, value]

  def _generate_cmd(self):
    cmd = [self.binary_path, '-d', 'start', '-logFile', self.local_logfile_path, self.key]
    for o in self.options.keys():
      if self.options.get(o) is not None:
        cmd = cmd + self.__xstr(o, self.options.get(o))
    return cmd

  def _generate_stop_cmd(self):
    cmd = self._generate_cmd()
    cmd[2] = 'stop'
    return cmd

  def start(self, **kwargs):
    self.options = kwargs

    if 'key' in self.options:
      self.key = self.options['key']
      del self.options['key']

    if 'binarypath' in self.options:
      self.binary_path = self.options['binarypath']
      del self.options['binarypath']
    else:
      self.binary_path = LocalBinary().get_binary()

    if 'logfile' in self.options:
      self.local_logfile_path = self.options['logfile']
      del self.options['logfile']

    if "onlyCommand" in kwargs and kwargs["onlyCommand"]:
      return

    self.proc = subprocess.Popen(self._generate_cmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = self.proc.communicate()

    os.system('echo "" > "'+ self.local_logfile_path +'"')
    try:
      if out:
        data = json.loads(out.decode())
      else:
        data = json.loads(err.decode())

      if data['state'] != "connected":
        raise BrowserStackLocalError(data["message"]["message"])
      else:
        self.pid = data['pid']
    except ValueError:
      raise BrowserStackLocalError('Error parsing JSON output from daemon')

  def isRunning(self):
    return hasattr(self, 'pid') and psutil.pid_exists(self.pid)

  def stop(self):
    try:
      proc = subprocess.Popen(self._generate_stop_cmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      (out, err) = proc.communicate()
    except Exception as e:
      return
