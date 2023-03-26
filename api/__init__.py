import os
import sys

# The PYTHONPATH directories and import statements were giving me absolute hell as I tried to both
# debug the code using Pycharms debugger and run the code in the production setting
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

