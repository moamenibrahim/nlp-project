import csv,re 

stopwords_file = open("./finnish_toolkit/finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()

with open('post_process/topics.txt', 'r') as in_file:
    topics_per_year = {}
    for line in in_file:
        if './post_process/time/' in line:
            try:
                time= re.match(r'\.\/[a-zA-Z*_*\/]*((\d+)-(\d+))\.txt', line.strip()).group(1)
                line=next(in_file)
                year=time.split('-')[1]
                elements = re.findall(r'\'([\wåäöÅÄÖ]+)\'', line.strip())
                if year not in topics_per_year:
                    topics_per_year[year] = {}

                for topic in elements:
                    # if topic in stopwords:
                    #     continue
                    if topic not in topics_per_year[year]:
                        topics_per_year[year][topic] = 1
                    else:
                        topics_per_year[year][topic] = topics_per_year[year][topic] + 1
            except:
                pass

    output = 'year,topic,count\n'
    for year in topics_per_year.keys():
        for topic in topics_per_year[year]:
            count = topics_per_year[year][topic]
            line = '{},{},{}\n'.format(year, topic, count)
            if count > 3: 
                output = output + line

    with open('./post_process/anan2.csv', 'w+') as f:
        f.write(output)

import pandas as pd
import matplotlib.pyplot as plt
df  = pd.read_csv("post_process/anan2.csv")
z=df['year']
n=df['count']
y=df['topic']
s= [float(2*v**2) for v in n]
fig, ax = plt.subplots()
ax.scatter(z, y, s=s)
# for i, txt in enumerate(n):
#     ax.annotate(txt, (z[i], y[i]))
plt.show()
print('done')