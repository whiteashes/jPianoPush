# jPianoPush - Python version

Pushing json structs from a log file dynamically read to a bridge. Random data generated with a gaussian distribution.

## Writing part
**writing.py** generates random data using a gaussian distribution. Mean and standard deviation are settable parameters. It is also possible to set an output range _bottom <= n <= top_. 
Predetermined string patterns have no intrinsic value; they are relatable to my curricular stage.

## Pushing part
**pushing.py** read dynamically from a log file in continous writing (thanks to _writing.py_). Every line passes through regex controls, and if there's a match data are parsed and written in a json structure (dictionary/nested dictionary). Finally, they are pushed with a HTTP POST request to a bridge/server/whatever you'd like capable to handle them.
