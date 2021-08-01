import substring
import misc


try:
    load_profile = open('/home/ubuntu/scripts/config.txt',"r")
    # load_profile = open('/home/david/Documents/Business/Projects/Python/config.txt',"r")
    read_it = load_profile.read()

    FileServerIPAddress=""
    ServerUsername=""
    ServerPassword=""
    DirOriginalImage=""
    DirCheckedImage=""
    DirBase64JSON=""
    DirPredictionJSON=""
    DirBackupOriginalImage=""
    DBServerIPAddress=""
    DBUsername=""
    DBPassword=""
    FileNamePrefix=""
    ImageKey=""

    for line in read_it.splitlines():
        if line.startswith("FileServerIPAddress="):
                FileServerIPAddress=line.split("=")[1].strip()
        if line.startswith("ServerUsername="):
                ServerUsername=line.split("=")[1].strip()
        if line.startswith("ServerPassword="):
                ServerPassword=line.split("=")[1].strip()
        if line.startswith("DirOriginalImage="):
                DirOriginalImage=line.split("=")[1].strip()
        if line.startswith("DirCheckedImage="):
                DirCheckedImage=line.split("=")[1].strip()
        if line.startswith("DirBase64JSON="):
                DirBase64JSON=line.split("=")[1].strip()
        if line.startswith("DirPredictionJSON="):
                DirPredictionJSON=line.split("=")[1].strip()
        if line.startswith("DirBackupOriginalImage="):
                DirBackupOriginalImage=line.split("=")[1].strip()
        if line.startswith("DBServerIPAddress="):
                DBServerIPAddress=line.split("=")[1].strip()
        if line.startswith("DBUsername="):
                DBUsername=line.split("=")[1].strip()
        if line.startswith("DBPassword="):
                DBPassword=line.split("=")[1].strip()
        if line.startswith("DatabaseName="):
                DatabaseName=line.split("=")[1].strip()
        if line.startswith("TensorflowPort="):
                TensorflowPort=line.split("=")[1].strip()
        if line.startswith("CCTVName="):
                CCTVName=line.split("=")[1].strip()
        if line.startswith("ImageKey="):
                ImageKey=line.split("=")[1].strip()

except Exception as e:
    misc.printerr("readconfig", e)
