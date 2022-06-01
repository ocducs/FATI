import os
import logging
import collections
from multiprocessing.pool import ThreadPool
from ._devices_mgr import DevicesMgr

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')


class _ADB:
    def __init__(self):
        self._pool = None

    def run(self, cmd, serials=None, is_shell_cmd=True, print_result=False):
        """
        :param cmd: adb shell command in shell mode, like 'ls -l'
        :param serials: by default is running on all connected device
        :param is_shell_cmd: to fish over stdout output
        """
        applied_serials = serials if serials else DevicesMgr.get_serials()

        if not self._pool:
            self._pool = ThreadPool(10)

        def _call_shell_cmd(s):
            if is_shell_cmd:
                full_cmd = 'adb -s {} shell "{}"'
            else:
                # non shell mode command needs to skip quote
                full_cmd = 'adb -s {} {}'
            full_cmd = full_cmd.format(s, cmd)
            
            logging.info('[ADB] Running command: ' + full_cmd)
            return os.popen(full_cmd).readlines()

        all_results = self._pool.map(_call_shell_cmd, applied_serials)
        adb_outputs_wrapper = collections.namedtuple('ADBstdout', ['serial', 'results'])
        adb_outputs = [adb_outputs_wrapper(*_) for _ in zip(applied_serials, all_results)]
        
        if print_result:
            for i in adb_outputs:
                logging.info('Results from device: ' + i.serial)
                for _l in i.results:
                    logging.info(_l.strip())
    
        return adb_outputs


ADB = _ADB()
