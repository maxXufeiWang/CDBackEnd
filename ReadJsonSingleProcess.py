import glob
import json
#handle file generation --> generating unique id --> could this be done with seesion id?
#

class Record:

    def removeRedundancy(self, evidence):
        if "_" == evidence[0]:
            evidence = ''+evidence[1:]
            return evidence
        elif "_" == evidence[-1]:
            evidence = evidence[:-1]
            return evidence
        elif "-" == evidence[0]:
            evidence = ''+evidence[1:]
            return evidence
        elif "-" == evidence[-1]:
            evidence = evidence[:-1]
            return evidence
        elif "-" in evidence:
            evidence = evidence.replace("-", "_")
            return evidence
        else:
            return evidence        

    def readCrypto(self, source):
        encryptionLib = []

        filename = open(source)
        data = json.load(filename)

        for SHA1_checksum in data ['crypto_evidence']:
            for index in range(0, len(data['crypto_evidence'][SHA1_checksum]['hits'])):

                encryption = data['crypto_evidence'][SHA1_checksum]['hits'][index]['matched_text']
                evidence = data['crypto_evidence'][SHA1_checksum]['hits'][index]['evidence_type']
                #if evidence == 'ethereum':
                encryption = self.removeRedundancy(str(encryption))
                if encryption.upper() not in encryptionLib:
                    encryptionLib.append(encryption.upper())
            
        #Writing .txt
        filename.close()

        print("Read complete")

        blockchain = "test"

        output = open(("cryptography.txt"), "w")

        output.write(f"Blockchain System: {blockchain}\n\n")
        for entries in encryptionLib:
            output.write(f"{entries}\n")
        output.close
        print("Output file has been generated")
