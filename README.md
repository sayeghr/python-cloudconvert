python-cloudconvert
===================

Python API for the CloudConvert.org service


__Currently the API is a mirror from the CloudConvert service, AKA just exposes their methds and is not usable in any easy way.__

### Requeriments
- python2.7 or python3 (_Should_ work in both)
- requests

### Example

    import CloudConvert
    
    apikey = "yourapikey"
    
    process = CloudConvert.ConversionProcess(apikey)
    
    # This should autodetect file extension. if not, you can
    # always set process.fromformat and .toformat to the correct
    # values
    process.init("/path/to/file.mp4", "path/to/output.m4v")
    
    # Will block until file is done processing. You can set
    # the interval between checks.
    process.wait_for_completion(interval=5)
    
    # Returns a file-like obj to download the processed file
    download = process.download()
    
    with open("output.m4v", "wb") as f:  # Important to set mode to wb
        f.write(download.read())
    


### Documentation

Help on module CloudConvert:

NAME
    CloudConvert

CLASSES
    builtins.object
        CloudConvert
        ConversionProcess

    class CloudConvert(builtins.object)
     |  Low level interface to the CloudConvert service
     |
     |  Methods defined here:
     |
     |  __init__(self, apikey)
     |
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |
     |  cancel(pid, host)
     |      Cancels the conversion methon ath any point.
     |      Currently there is no way of resuming
     |
     |  conversion_types(inputformat=None, outputformat=None)
     |      Returns a dict with all te possible conversions and
     |      conversion specific options.
     |
     |      Arguments:
     |          inputformat(str) -> input format to lookup [optional]
     |          outputformat(str) -> outpu format to lookup [optional]
     |
     |  delete(pid, host)
     |      Deletes files of a conversion process
     |
     |  download(pid, host)
     |      Returns a file-like object containing the file
     |
     |  list(apikey)
     |      Returns the history of the conversions of the supplied apikey.
     |
     |  start(inputformat, outputformat, apikey)
     |      Inits the process in the remote server
     |
     |  status(pid, host)
     |      Checks the conversion status of a process
     |
     |  upload(fname, outformat, pid, host, options=None)
     |      Uploads a file to be converted
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

    class ConversionProcess(builtins.object)
     |  Methods defined here:
     |
     |  __init__(self, apikey)
     |
     |  cancel(self)
     |      Cancels the process. Currently there is no way of resuming.
     |
     |  delete(self)
     |      Deletes the files from the current process.
     |
     |      Note: files will get automatically deleted after a fixed period of time
     |          available trough status()
     |      Note: if the process is alredy running, it's first cancelled
     |
     |  download(self)
     |      Returns a file-like object with the output file, fro download.
     |
     |  init(self, fromfile, tofile)
     |      Prepares the conversion
     |
     |  start(self)
     |      Uploads the file hence starting the conversion process
     |
     |  status(self)
     |      Returns the status of the process
     |
     |  wait_for_completion(self, check_interval=1)
     |      This blocks until the process status["step"] changes to "finished".
     |
     |      Arguments:
     |          check_interval(int) -> seconds to wait between each check.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)