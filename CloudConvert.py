import requests
import time


class CloudConvert():
    """
    Low level interface to the CloudConvert service
    """

    def __init__(self, apikey):
        """
        apikey(str) -> The api key from CloudConvert
        """
        self.apikey = apikey
        self.pid = None

    def _start(self, inputformat, outputformat, apikey=None):
        if apikey is None:
            apikey = self.apikey

        url = (
            "https://api.cloudconvert.org/process?"
            "inputformat={inputf}&outputformat={outputf}&apikey={api}"
            ).format(
            inputf=inputformat,
            outputf=outputformat,
            api=self.apikey)

        return requests.get(url).text

    def _upload(self, fname, outformat, pid=None, options=None):
        if pid is None:
            pid = self.pid

        url = (
            "https://srv01.cloudconvert.org/process/{pid}"
            ).format(pid=pid)

        if options is None:
            options = {}  # TODO

        with open(fname, "r") as f:
            requests.post(url,
                          data={
                              "outputformat": outformat
                              },
                          files={"file": f})

    def _status(self, pid=None):
        if pid is None:
            pid = self.pid

        url = (
            "https://srv01.cloudconvert.org/process/{pid}"
            ).format(pid=pid)

        return requests.get(url).json()

    def _download(self, pid=None):
        if pid is None:
            pid = self.pid

        url = self._status(pid)["output"]["url"]

        return requests.get(url, stream=True)

    def _cancel(self, pid=None):
        if pid is None:
            pid = self.pid

        url = (
            "https://srv01.cloudconvert.org/process/{pid}/cancel"
            ).format(pid=pid)

        requests.get(url)

    def _delete(self, pid=None):
        if pid is None:
            pid = self.pid

        url = (
            "https://srv01.cloudconvert.org/process/{pid}/delete"
            ).format(pid=pid)

        requests.get(url)

    def list(self, apikey=None):
        """
        Returns the history of the conversions of the current
        apikey.

        You can specify a different apikey.
        """
        if apikey is None:
            apikey = self.apikey

        url = (
            "https://api.cloudconvert.org/processes?apikey={api}"
            ).format(api=apikey)

        return requests.get(url).json()

    def conversion_types(self, inputformat=None, outputformat=None):
        """
        Returns a dict with all te possible conversions and
        conversion specific options.

        Arguments:
            inputformat(str) -> input format to lookup [optional]
            outputformat(str) -> outpu format to lookup [optional]
        """
        kwargs = {"inputformat": inputformat,
                  "outputformat": outputformat}

        url = "https://api.cloudconvert.org/conversiontypes"

        if inputformat or outputformat:
            toappend = [param+"="+kwargs[param]
                        for param in kwargs
                        if kwargs[param] is not None]
            url += "?" + "&".join(toappend)

        return url


class ConversionProcess(CloudConvert):
    def __init__(self, apikey):
        super().__init__(apikey)

        self.pid = None

        self.fromfile = None
        self.fromformat = None

        self.tofile = None
        self.toformat = None

    def _get_format(self, f):
        return f.split(".")[-1]

    def init(self, fromfile, tofile):
        """
        Prepares the conversion
        """
        self.fromfile = fromfile
        self.tofile = tofile

        # If this doesn't get resolved right,
        # user has to provide the correct ones.
        self.fromformat = self._get_format(fromfile)
        self.toformat = self._get_format(tofile)

        self.pid = self._start(self.fromformat, self.toformat)
        return self.pid

    def start(self):
        """
        Uploads the file hence starting the conversion process
        """
        self._upload(self.fromfile, self.fromformat)

    def status(self):
        """
        Returns the status of the process
        """
        # TODO: Make it more beautiful, not just raw json response
        return self._status()

    def cancel(self):
        """
        Cancels the process. Currently there is no way of resuming.
        """
        self._cancel()

    def delete(self):
        """
        Deletes the files from the current process.
        
        Note: files will get automatically deleted after a fixed period of time
            available trough status()
        Note: if the process is alredy running, it's first cancelled
        """
        self._delete()

    def wait_for_completion(self, check_interval=1):
        """
        This blocks until the process status["step"] changes to "finished".

        Arguments:
            check_interval(int) -> seconds to wait between each check.
        """
        while True:
            time.sleep(check_interval)
            if self._status()["step"] == "finished":
                break

    def download(self):
        """
        Returns a file-like object with the output file, fro download.
        """
        # File-like object
        return self._download().raw
