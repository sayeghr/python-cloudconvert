python-cloudconvert
===================

Python API for the CloudConvert.org service

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

    process.start()
    
    # Will block until file is done processing. You can set
    # the interval between checks.
    process.wait_for_completion(check_interval=5)
    
    # Returns a file-like obj to download the processed file
    download = process.download()
    
    with open("output.m4v", "wb") as f:  # Important to set mode to wb
        f.write(download.read())
    


### Documentation

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
     |  cancel(process_url)
     |      Cancels the conversion methon at any point.
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
     |  delete(process_url)
     |      Deletes files of a conversion process
     |
     |  download(process_url)
     |      Returns a file-like object containing the file
     |
     |  list(apikey)
     |      Returns the conversion history of the supplied apikey.
     |
     |  start(inputformat, outputformat, apikey)
     |      Inits the process in the remote server
     |
     |  status(process_url)
     |      Checks the conversion status of a process
     |
     |  upload(fname, outformat, process_url, options=None)
     |      Uploads a file to be converted
     |
     |  ----------------------------------------------------------------------

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
     |      Returns a file-like object with the output file, for download.
     |
     |  init(self, fromfile, tofile)
     |      Prepares the conversion
     |
     |  is_possible(self)
     |      Checks if there is a conversion type between the two formats.
     |      Returns boolean.
     |
     |  save(self)
     |      Saves the output with the designated filename and extension
     |
     |  start(self)
     |      Uploads the file hence starting the conversion process
     |
     |  status(self)
     |      Returns the status of the process
     |
     |  wait_for_completion(self, check_interval=1)
     |      This blocks until the process status["step"] changes to "finished"
     |      when returns True or "error", in which case, returns False.
     |
     |      If there is an error other than the conversion failing,
     |      it will raise 'ConversionProcessException'
     |
     |      Arguments:
     |          check_interval(int) -> seconds to wait between each check.
     |
     |  ----------------------------------------------------------------------
