import os
import shutil

def deleteTempFiles(sessionID):
    if os.path.exists('cryptoes\\' + sessionID + ".crypto"):
        os.remove('cryptoes\\' + sessionID + ".crypto")
        if os.path.exists('storage\\' + sessionID):
            shutil.rmtree('storage\\' + sessionID)
            print("temp storage dir deleted.")
        print("temp .crypto file deleted.")
    else:
        print("The file does not exist")

