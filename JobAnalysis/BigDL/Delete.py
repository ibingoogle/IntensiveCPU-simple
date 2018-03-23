import os
import sys

delete_command = "rm -rf /opt/modules/bigdl-master-angelps/executioninfo/timefile* 2>/dev/null"
print delete_command
os.popen(delete_command)
