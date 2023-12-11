from datetime import datetime

def formatTiem(time = datetime.now(), mode = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(mode)

