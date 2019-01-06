import csv,re 

with open('post_process/topics.txt', 'r') as in_file:
    myline=[]
    for line in in_file:
        if './post_process/time/' in line:
            try:
                time= re.match(r'\.\/[a-zA-Z*_*\/]*((\d+)-(\d+))\.txt', line.strip()).group(1)
                # myline.append(time)
                line=next(in_file)
                myline.append([time,line.strip().split(",")])
            except:
                pass

    with open('post_process/topics.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('time', 'topics'))
        writer.writerows(myline)