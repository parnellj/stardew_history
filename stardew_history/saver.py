import os
import shutil
import datetime as dt

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

indir = r'C:\Users\Justin\AppData\Roaming\StardewValley\Saves'
outdir = os.path.join('.', 'backups')


def createDir(testDir):
    if not os.path.exists(testDir):
        os.mkdir(testDir)
    return testDir


class MyHandler(PatternMatchingEventHandler):
    # http://brunorocha.org/python/
    # watching-a-directory-for-file-changes-with-python.html

    def process(self, event):
        parentFolder = os.path.split(os.path.dirname(os.path.normpath(event.src_path)))[1]
        targetPath, targetFile = os.path.split(os.path.normpath(event.src_path))
        fileParentName = os.path.split(targetPath)[1]
        print 'event of type:' + str(event.event_type)
        if event.event_type in ['created', 'modified']:
            if event.is_directory:
                createDir(os.path.join(outdir, targetFile))
            elif 'STARDEWVALLEYSAVETMP' not in event.src_path and '_old' not in event.src_path:
                prefix = 'SGI_' if targetFile == 'SaveGameInfo' else 'SAV_'
                out_file = os.path.join(outdir, parentFolder, prefix + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                open(out_file, 'w').close()
                try:
                    print 'copying ' + str(event.src_path) + ' => ' + str(out_file)
                    shutil.copyfile(event.src_path, out_file)
                except IOError:
                    print 'print didn\'t work :('

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    event_handler = MyHandler()
    print 'scanning ' + indir
    observer = Observer()
    observer.schedule(event_handler, indir, recursive=True)
    observer.start()
    observer.join()
