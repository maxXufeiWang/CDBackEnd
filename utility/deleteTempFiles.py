import os
import shutil

def deleteTempFiles(sessionID):
    print("Clearing temp folders and files:")
    if os.path.exists('cryptoes\\' + sessionID + ".crypto"):
        os.remove('cryptoes\\' + sessionID + ".crypto")
        if os.path.exists('storage\\' + sessionID):
            shutil.rmtree('storage\\' + sessionID)
            print("\tTemp storage dir deleted.")
        print("\ttemp .crypto file deleted.")
    else:
        print("The file does not exist")
        return
    print("Clearing process finished.")

