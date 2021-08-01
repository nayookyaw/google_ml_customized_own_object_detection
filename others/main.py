import os
import pyinotify
import datetime
import readconfig
import process
import misc
import uuid
import mysqlDb


class EventProcessor(pyinotify.ProcessEvent):
    _methods = ["IN_CREATE",
                "IN_OPEN",
                "IN_ACCESS",
                "IN_ATTRIB",
                "IN_CLOSE_NOWRITE",
                "IN_CLOSE_WRITE",
                "IN_DELETE",
                "IN_DELETE_SELF",
                "IN_IGNORED",
                "IN_MODIFY",
                "IN_MOVE_SELF",
                "IN_MOVED_FROM",
                "IN_MOVED_TO",
                "IN_Q_OVERFLOW",
                "IN_UNMOUNT",
                "default"]


rawfile = ""


def process_generator(cls, method):
    def _method_name(self, event):
        try:
            global rawfile
            rawfile = event.pathname
            ts = datetime.datetime.now()
            tsfmt = ts.strftime("%Y%m%d-%H%M%S.%f")

            if event.mask == pyinotify.IN_CLOSE_WRITE or event.mask == pyinotify.IN_CREATE:
                print("Time : {} | Event : {} | Path name : {}".format(tsfmt, event.maskname, rawfile))
    
            if event.mask == pyinotify.IN_CLOSE_WRITE:
                # Slot in uuid for primary key in MySQL tables
                uuid_value = str(uuid.uuid1())

                # Adding Original file creation timestamp to be added to all file names 
                creationTS = datetime.datetime.fromtimestamp(os.path.getctime(rawfile)) 

                print("uuid: %s" % uuid_value)
                print("timestamp: %s" % str(creationTS))

                # Insert into db
                mysqlDb.mysql_data_input_folderA(uuid_value, rawfile)

                # resize image to 500x500
                process.resizeImage(uuid_value, creationTS, rawfile)

                # save metadata
                # process.saveResizedMetadata()

                # move raw file to folder 0
                process.movefile(rawfile)

                # convert image to Base64 encoding and save it as a json file
                process.convertImage(uuid_value, creationTS)

                # closing
                print("")
                print("")

        except Exception as e:
            misc.printerr("_method_name", e)

    try:
        _method_name.__name__ = "process_{}".format(method)
        setattr(cls, _method_name.__name__, _method_name)

    except Exception as e:
        misc.printerr("process_generator", e)


def delete_temp_file(file):
    try:
        if os.path.exists(file):
            os.remove(file)

    except Exception as e:
        misc.printerr("delete_temp_file", e)




try:

    # remove pid and log files
#    delete_temp_file("/tmp/mydaemon.pid")
    delete_temp_file("/tmp/error.log")
    delete_temp_file("/tmp/out.log")

    for method in EventProcessor._methods:
        process_generator(EventProcessor, method)

    watch_manager = pyinotify.WatchManager()
    event_notifier = pyinotify.Notifier(watch_manager, EventProcessor())
    watch_this = os.path.abspath(readconfig.DirOriginalImage)

    watch_manager.add_watch(watch_this, pyinotify.IN_CREATE
                            | pyinotify.IN_ACCESS | pyinotify.IN_ATTRIB | pyinotify.IN_CLOSE_NOWRITE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE
                            | pyinotify.IN_DELETE_SELF | pyinotify.IN_IGNORED | pyinotify.IN_MODIFY | pyinotify.IN_MOVE_SELF | pyinotify.IN_MOVED_FROM
                            | pyinotify.IN_MOVED_TO | pyinotify.IN_Q_OVERFLOW | pyinotify.IN_UNMOUNT)

    event_notifier.loop(daemonize=True, pid_file='/tmp/mydaemon.pid', stdout='/tmp/out.log', stderr='/tmp/error.log')

except Exception as e:

    misc.printerr("main", e)
