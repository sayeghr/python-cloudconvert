import requests
import time


class CloudConvert():

    """
    Low level interface to the CloudConvert service
    """

    @staticmethod
    def start(inputformat, outputformat, apikey):
        """
        Inits the process in the remote server
        """

        url = (
            "https://api.cloudconvert.org/process?"
            "inputformat={inputf}&outputformat={outputf}&apikey={api}"
        ).format(
            inputf=inputformat,
            outputf=outputformat,
            api=apikey)

        return requests.get(url).json()

    @staticmethod
    def upload(fname, outformat, process_url, options=None):
        """
        Uploads a file to be converted
        """

        if options is None:
            options = {}  # TODO

        with open(fname, "rb") as f:
            requests.post(process_url,
                          data={
                              "outputformat": outformat
                          },
                          files={"file": f})

    @staticmethod
    def status(process_url):
        """
        Checks the conversion status of a process
        """

        return requests.get(process_url).json()

    @staticmethod
    def download(process_url):
        """
        Returns a file-like object containing the file
        """

        url = "https:" + CloudConvert.status(process_url)["output"]["url"]

        return requests.get(url, stream=True).raw

    @staticmethod
    def cancel(process_url):
        """
        Cancels the conversion methon at any point.
        Currently there is no way of resuming
        """

        url = (
            "{purl}/cancel"
        ).format(purl=process_url)

        requests.get(url)

    @staticmethod
    def delete(process_url):
        """
        Deletes files of a conversion process
        """

        url = (
            "{purl}/delete"
        ).format(purl=process_url)

        requests.get(url)

    @staticmethod
    def list(apikey):
        """
        Returns the conversion history of the supplied apikey.
        """

        url = (
            "https://api.cloudconvert.org/processes?apikey={api}"
        ).format(api=apikey)

        return requests.get(url).json()

    @staticmethod
    def conversion_types(inputformat=None, outputformat=None):
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
            toappend = [param + "=" + kwargs[param]
                        for param in kwargs
                        if kwargs[param] is not None]
            url += "?" + "&".join(toappend)

        return requests.get(url).json()


class ConversionProcessException(Exception):
    pass


class ConversionProcess():

    def __init__(self, apikey):
        self.apikey = apikey

        self.url = None

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

        j = CloudConvert.start(self.fromformat, self.toformat, self.apikey)
        self.url = "https:" + j["url"]

        return j["id"]  # pid

    def is_possible(self):
        """
        Checks if there is a conversion type between the two formats.
        Returns boolean.
        """

        if self.fromformat is None or self.toformat is None:
            return False

        else:
            return bool(
                CloudConvert.conversion_types(
                    inputformat=self.fromformat,
                    outputformat=self.toformat
                )
            )

    def start(self):
        """
        Uploads the file hence starting the conversion process
        """

        CloudConvert.upload(
            self.fromfile, self.fromformat, self.url)

    def status(self):
        """
        Returns the status of the process
        """

        # TODO: Make it more beautiful, not just raw json response
        return CloudConvert.status(self.url)

    def cancel(self):
        """
        Cancels the process. Currently there is no way of resuming.
        """

        CloudConvert.cancel(self.url)

    def delete(self):
        """
        Deletes the files from the current process.

        Note: files will get automatically deleted after a fixed period of time
            available trough status()
        Note: if the process is alredy running, it's first cancelled
        """

        CloudConvert.delete(self.url)

    def wait_for_completion(self, check_interval=1):
        """
        This blocks until the process status["step"] changes to "finished"
        when returns True or "error", in which case, returns False.

        If there is an error other than the conversion failing,
        it will raise 'ConversionProcessException'

        Arguments:
            check_interval(int) -> seconds to wait between each check.
        """

        while True:
            time.sleep(check_interval)

            status = self.status()

            if status.get("error", False):
                raise ConversionProcessException(status["error"])

            step = status["step"]
            if step == "finished":
                return True
            elif step == "error":
                return False

    def download(self):
        """
        Returns a file-like object with the output file, for download.
        """

        # File-like object
        return CloudConvert.download(self.url)

    def save(self):
        """
        Saves the output with the designated filename and extension
        """

        download = self.download()

        with open(self.tofile, "wb") as f:  # Important to set mode to wb
            f.write(download.read())
