def read_history():
    '''
    line - строка ф файле такого же вида, что и intervals
    '''
    result = ''
    with open('./volume/history.txt', 'r') as f:
        line = f.readline()
        last_time, last_status = line.split(',')
        last_status = last_status.strip()
        last_time_start, last_time_end = last_time.split('-')
        time_start = ''
        time_end = ''
        status = ''
        while line:
            
            time_interval, status = line.split(',')
            status = status.strip()
            time_start, time_end = time_interval.split('-')
            
            if (last_status == status):
                last_time_end = time_end
            else:
                result += f"[{last_time_start}-{last_time_end}: {last_status.strip()}]\n"
                last_time_start = time_start
                last_time_end = time_end
                last_status = status
            line = f.readline()
        result += f"[{last_time_start}-{last_time_end}: {last_status.strip()}]\n"
    return result

def update_history(time_start, time_end, new_status):
    with open('./volume/history.txt', 'a') as f:
        string = f"{time_start}-{time_end},{new_status}\n"
        f.write(string)