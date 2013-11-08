import requests


class CloudConvert():
    def __init__(self, apikey):
        self.apikey = apikey

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

    def _upload(self, pid, fname, outformat, options=None):
        url = (
            "https://srv01.cloudconvert.org/process/{pid}"
            ).format(pid=pid)

        if options is None:
            options = {}

        with open(fname, "r") as f:
            requests.post(url,
                          data={
                              "outputformat": outformat
                              },
                          files={"file": f})

    def _status(self, pid):
        url = (
            "https://srv01.cloudconvert.org/process/{pid}"
            ).format(pid=pid)

        return requests.get(url).json()

    def _cancel(self, pid):
        url = (
            "https://srv01.cloudconvert.org/process/{pid}/cancel"
            ).format(pid=pid)

        requests.get(url)

    def _delete(self, pid):
        url = (
            "https://srv01.cloudconvert.org/process/{pid}/delete"
            ).format(pid=pid)

        requests.get(url)

    def _list(self, apikey=None):
        if apikey is None:
            apikey = self.apikey

        url = (
            "https://api.cloudconvert.org/processes?apikey={api}"
            ).format(api=apikey)
        print url

        return requests.get(url).json()