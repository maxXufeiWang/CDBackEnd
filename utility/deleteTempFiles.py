import os
import shutil

def deleteTempFiles(sessionID):
    print("Clearing temp folders and files:")
    
    if os.path.exists('storage\\' + sessionID):
        shutil.rmtree('storage\\' + sessionID)
        print("\tTemp storage dir deleted.")
    
    print("Clearing process finished.")

