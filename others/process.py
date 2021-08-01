from __main__ import *

import json
import time
import misc
import mysqlDb


print("start process")

resizedFile = ""
jsonBase64Path = ""


def movefile(rawfile):
    try:
        fp = os.path.split(rawfile)
        newfile = readconfig.DirBackupOriginalImage + "/" + fp[1]
        os.rename(rawfile,newfile)
        print("Move %s to %s" % (rawfile, newfile))

    except Exception as e:
        misc.printerr("movefile", e)


def resizeImage(uuid_value, creationTS, rawfile):
    import sys
    from resizeimage import resizeimage 
    from PIL import Image

    try:
        with open(rawfile, 'rb') as f:
            with Image.open(f) as image:
                global resizedFile
                resizedFile = "%s/%s-%s.jpg" % (readconfig.DirCheckedImage, readconfig.CCTVName, creationTS.strftime("%Y%m%d%H%M%S"))
                cover = resizeimage.resize_thumbnail(image, [500, 500])
                cover.save(resizedFile, image.format)

                # Insert into db
                mysqlDb.mysql_data_input_folderB(uuid_value, resizedFile)

                print("Resize image of %s to %s" % (rawfile, resizedFile))

    except Exception as e:
        print(e)
        misc.printerr("resizeImage", e)


def saveResizedMetadata():
    try:
        if os.path.exists(resizedFile):
            fileSize = os.path.getsize(resizedFile)
            fileTime = datetime.datetime.fromtimestamp(os.path.getctime(resizedFile))
            json_value = "{\"filename\" : \"" + resizedFile + "\", \"filesize\" : \"" + str(fileSize) + "\", \"timestamp\" : \"" + fileTime.strftime("%Y%m%d%H%M%S") +"\"}"
            mysqlDb.mysql_data_input(json_value, 'metadatadocs')
            print("Save metadata of %s" % (resizedFile))
        else:
            print("Cannot find the resized file \"%s\"" % (resizedFile))

    except Exception as e:
        misc.printerr("saveResizedMetadata", e)


def convertImage(uuid_value, creationTS):
    try:
        import base64
        import substring
        import shutil
        import mysqlx
        import requests

        with open(resizedFile, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # json_value =" { \"instances\" : [ { \"image_bytes\" : { \"b64\" :\"" + encoded_string + "\" }, \"key\" :\"" + readconfig.ImageKey + "\" } ] }" 
        json_value =' { "instances" : [ { "image_bytes" : { "b64" :"' + encoded_string + '" }, "key" : "' + readconfig.ImageKey + '" } ] }'

        json_file_name = readconfig.CCTVName + "-" + creationTS.strftime("%Y%m%d%H%M%S") + ".json"
        global jsonBase64Path
        jsonBase64Path = readconfig.DirBase64JSON + "/" + json_file_name 
        with open(jsonBase64Path, 'w') as outfile:
            # json.dump(json_value, outfile)
            outfile.write(json_value) 
            outfile.close()

        # Insert into db
        mysqlDb.mysql_data_input_folderC(uuid_value, jsonBase64Path)

        print("Convert image of %s to %s" % (resizedFile, jsonBase64Path))

        # Send to tensorflow and save it to json file
        url = 'http://localhost:{}/v1/models/default:predict'.format(readconfig.TensorflowPort)

        response = requests.post(url, data = json_value)
        json_pred_file_name = readconfig.CCTVName + "-" + creationTS.strftime("%Y%m%d%H%M%S") + ".json"
        jsonPredPath = readconfig.DirPredictionJSON + "/" + json_pred_file_name
        json_pred = str(response.json())
        json_string = json_pred.replace("'","\"")
        print(json_string)
#        json_pred = "{}"
        with open(jsonPredPath, 'w') as outfile:
            outfile.write(json_string)
            outfile.close()

        # Insert into db
        mysqlDb.mysql_data_input_folderD(uuid_value, jsonPredPath,json_string)

        #print(response.json()) 
        print("Save response from TensorFlow as %s" % jsonPredPath)

    except Exception as e:
        misc.printerr("convertImage", e)


'''
def json2db():
    try:
        load_profile=open(jsonBase64Path,"r").read()
        json_value=json.loads(load_profile)
        mysqlDb.mysql_data_input(json_value,'base64docs')
        print("Save json file of %s to db" % (jsonBase64Path))

    except Exception as e:
        misc.printerr("json2db", e)
'''
