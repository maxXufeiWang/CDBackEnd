from fileinput import filename

class algEngine(object):
    def __init__(self, path):
        # Setup
        fileNames = self.get_file_name(path)
        self.database = self.generate_db(path, fileNames)

    def get_file_name(self, path):
        import os

        retList = []
        path = os.path.abspath(path)

        for file in os.listdir(path): 
            retList.append(file)

        return retList

    # Building a list of dict as referencing database
    # keys are bType(blockchain type), libName(encryption library name), and chance(possibility associated with that library)
    def generate_db(self, path, fileNames):
        files = []
        for name in fileNames:
            files.append(open(path + "\\\\" + name, "rb"))

        db = []
        for f in files:
            content = f.read()
            row = self.extract_db_content(content)
            db = db + row

        return db
    
    def extract_db_content(self, content):
        results = content.split( )

        # ignore header
        results = results[6:]
        
        tempRow = []
        for result in results:
            result = result.decode().split(":")
            if(len(result) == 3):
                tempRow.append({"bType":result[0], "libName":result[1], "chance":result[2]})

        return tempRow

    # function caller
    def process_upload(self, data):
        type, data = self.extract_file_content(data)
        libraries = self.find_file_library(type, data)
        libraries = self.exclude_unrelated(libraries)
        chances = self.check_for_chance(libraries)
        retBody = self.prepare_ret(chances)

        return retBody

    # decode file and return the text contained in it
    def extract_file_content(self, data):
        data = data.decode()
        data = str(data).splitlines()
        
        filetype = str(data[1]).split("filename=")[1].split("\"")[1].split(".")[1]
        data = data[4:]
        data = data[:len(data) - 1]

        return filetype, data

    # extract libraries included in the source code.
    # TODO : currently only read python. Add more languages here.
    def find_file_library(self, type, data):
        result = []
        if (type == "py"):
            for d in data:
                if "import" in d:
                    lst = d.split(" ")
                    if "from" in lst: 
                        result.append(lst[lst.index("from") + 1])

                    elif "import" in lst: 
                        result.append(lst[lst.index("import") + 1])
        return result

    # exclude the libraries that are not in our reference database
    # to avoid contamination
    def exclude_unrelated(self, libraries):
        retList = []

        for library in libraries:
            for db in self.database:
                if library == db["libName"]:
                    retList.append(library)

        return retList

    # calculate chances by matching related libraries with referencing database.
    def check_for_chance(self, libraries):
        print(libraries)
        result = []
        length = len(libraries)
    
        for lib in libraries:
            for entry in self.database:
                if lib == entry["libName"]:
                    bExisted = False
                    chance = float(entry["chance"])

                    for r in result:
                        if(r["bType"] == entry["bType"]):
                            bExisted = True
                            r["chance"] = r["chance"] + chance / length

                            break
                    
                    if not bExisted:
                        result.append({"bType": entry["bType"], "chance": chance / length})
                        print(result)
    
        return self.normalize_chance(result)

    # Make the total = 100
    def normalize_chance(self, chances):
        total = 0

        for i in range(len(chances)):
            chances[i]["chance"] = round(chances[i]["chance"] * 100, 1)
            total += chances[i]["chance"]

        if total < 100:
            chances.append({"bType": "Unknown", "chance": 100 - total})
        elif total > 100:
            tempT = 0
            for i in range(len(chances)):
                if i != len(chances) - 1:
                    temp = round(chances[i]["chance"] / total)
                    tempT += temp
                else:
                    temp = 100 - tempT
                
                chances[i]["chance"] = temp
                 
        return chances

    # Build return body
    def prepare_ret(self, chances):
        if(len(chances) == 0):
            retBody = {"code": 404, "msg": "Sorry, no match found."}

        else:
            retBody = {"code": 333, "data": chances}

        s = " import GNUPG "
        s = " import D2IASRANGE "

        return retBody