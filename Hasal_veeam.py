import os
import hashlib
import time

LOG = 'log.txt'


# function area
# -------------------------------------------------------------

# log function
def log(message):
    # write log
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(LOG, 'a') as f:
        f.write('['+now+']'+message+'\n')


# compare 2 files with hash
def compare2file(file1, file2):
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False

# compare hash folder
# return True if all file is same
# return False if any file is different
def compareHashFolder(folder, backup):
     # get all file in folder
    files = os.listdir(folder)
    # get all file in backup
    files_backup = os.listdir(backup)
    # compare 2 list
    if len(files) != len(files_backup):
        return False

    for file in files:
        if file in files_backup:
            if not compare2file(folder+'/'+file, backup+'/'+file):
                return False
        else:
            return False
    return True

#------------------------------------------------------------------
log('Start')

folder = input('put your origin path:')
backup = input('put your copy path:')
# check if folder is exist
if not os.path.isdir(folder):
    log('folder: NOT FOUND')
    print('folder is not exist')
    exit()
# check if backup is exist
if not os.path.isdir(backup):
    log('backup: NOT FOUND')
    print('backup is not exist')
    exit()

# run loop every x sec
loop_time = input('put synchronization interval in sec:')

while True:
    # check if folder is same with backup
    if compareHashFolder(folder, backup):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'[{now}] file is up to date')
        log('file is up to date')
        # sleep for x sec
        time.sleep(int(loop_time))
        continue    

    # check folder
    if os.path.isdir(folder):
        print('folder: ONLINE')
        log('folder: ONLINE')
    else:
        print('folder is not exist')
        log('folder is not exist')
        print('please check your config file')
        break

    # check backup
    if os.path.isdir(backup):
        print('backup: ONLINE')
        log('backup: ONLINE')
    else:
        print('backup is not exist')
        log('backup is not exist')
        print('please check your config file')
        break

    # check file hash in folder and compare with backup
    countSync = 0
    updateFile = 0
    deleteFile = 0

    # get all file in folder
    files = os.listdir(folder)
    # get all file in backup
    files_backup = os.listdir(backup)
    # compare 2 list
    for file in files_backup:
        if file in files:
            if compare2file(folder+'/'+file, backup+'/'+file):
                log(f'{file} is up to date')
                countSync += 1
            else:
                # copy file from folder to backup
                updateFile += 1
                os.remove(backup+'/'+file)
                os.system('copy '+folder+'/'+file+' '+backup)
                
                log(f'{file} is updated')
        if file not in files:
            # delete file in backup
            log(f'{file} is deleted')
            deleteFile += 1
            os.remove(backup+'/'+file)

    for file in files:
        if file not in files_backup:
            # copy file from folder to backup
            updateFile += 1
            log(f'{file} is copied')
            os.system('copy '+folder+'/'+file+' '+backup)



    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log(f'[{now}] sync: {countSync}; update: {updateFile}; delete: {deleteFile};')
    print(f'[{now}] sync: {countSync}; update: {updateFile}; delete: {deleteFile};')

    # sleep for x sec
    time.sleep(int(loop_time))