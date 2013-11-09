python-cloudconvert
===================

Python API for the CloudConvert.org service


__Currently the API is a mirror from the CloudConvert service, AKA just exposes their methds and is not usable in any easy way.__

### Requeriments
- python2.7 or python3 (_Should_ work in both)
- requests


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
         |      apikey(str) -> The api key from CloudConvert
         |  
         |  conversion_types(self, inputformat=None, outputformat=None)
         |      Returns a dict with all te possible conversions and
         |      conversion specific options.
         |      
         |      Arguments:
         |          inputformat(str) -> input format to lookup [optional]
         |          outputformat(str) -> outpu format to lookup [optional]
         |  
         |  list(self, apikey=None)
         |      Returns the history of the conversions of the current
         |      apikey.
         |      
         |      You can specify a different apikey.
         |  
         |  ----------------------------------------------------------------------
        
        class ConversionProcess(CloudConvert)
         |  Method resolution order:
         |      ConversionProcess
         |      CloudConvert
         |      builtins.object
         |  
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
         |  Methods inherited from CloudConvert:
         |  
         |  conversion_types(self, inputformat=None, outputformat=None)
         |      Returns a dict with all te possible conversions and
         |      conversion specific options.
         |      
         |      Arguments:
         |          inputformat(str) -> input format to lookup [optional]
         |          outputformat(str) -> outpu format to lookup [optional]
         |  
         |  list(self, apikey=None)
         |      Returns the history of the conversions of the current
         |      apikey.
         |      
         |      You can specify a different apikey.
