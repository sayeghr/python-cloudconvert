import os
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

import CloudConvert

apikey = open("apikey.txt", "r").read().strip()

process = CloudConvert.ConversionProcess(apikey)

process.init("test_doc.rtf", "out.txt")

print("from", process.fromformat)
print("to", process.toformat)
print("possible?", process.is_possible())

print("start")
process.start()

print("waiting")
process.wait_for_completion()

print("Saving")
process.save()
