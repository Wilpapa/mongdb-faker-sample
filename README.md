# mongdb-faker-sample
Sample python code to generate fake MongoDB data using single and multiple processes

Files
-----

- fakerFR-multiprocess.py : multiprocess version
- (single process version soon)

Usage
----

- edit variables :

#Number of processes to simultaneously

``processesNumber = 16``

#Locale Settings for Faker (see https://github.com/joke2k/faker)

``fake = Factory.create('fr_FR') # using french names, cities, etc.``

#batch size (total number of documents to write) and bulk size (number of docs to write simultaneously)

``batchSize=1000000``

``bulkSize=1000``

- launch the script

``$ python fakerFR-multiprocess.py``

- in another shell, launch mongostat to follow the writes (1st column)

```
insert query update delete getmore command dirty used flushes vsize  res qrw arw net_in net_out conn                time
 18507    *0     *0     *0       0     2|0  1.1% 1.2%       0 3.25G 137M 0|0 1|0  4.69m   52.9k   33 Jan 31 16:00:27.260
 32088    *0     *0     *0       0     2|0  1.2% 1.3%       0 3.25G 147M 0|0 1|0  8.49m   51.7k   33 Jan 31 16:00:28.257
 32022    *0     *0     *0       0    18|0  1.4% 1.4%       0 3.27G 159M 0|0 1|0  8.45m   54.9k   33 Jan 31 16:00:29.257
 31886    *0     *0     *0       0     1|0  1.6% 1.6%       0 3.28G 170M 0|0 1|0  8.41m   51.4k   33 Jan 31 16:00:30.260
 32345    *0     *0     *0       0     2|0  1.7% 1.7%       0 3.29G 181M 0|0 1|0  8.52m   52.1k   33 Jan 31 16:00:31.249
```

