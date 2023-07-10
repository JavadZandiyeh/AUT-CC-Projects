hdfs dfs -rm -r /user/root/output/*

cd jars
cat ../data/dataset.csv | python3 mapper1.py | sort -k1,1 | python3 reducer1.py
cat ../data/dataset.csv | python3 mapper2.py | sort -k1,1 | python3 reducer2.py
cat ../data/dataset.csv | python3 mapper3.py | sort -k1,1 | python3 reducer3.py

hdfs dfs -rm -r /user/root/output/part1
hadoop jar /opt/hadoop-3.3.1/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -file /app/jars/mapper1.py -mapper "python3 mapper1.py" -file /app/jars/reducer1.py -reducer "python3 reducer1.py" -input /user/root/input/dataset.csv -output /user/root/output/part1
hdfs dfs -cat /user/root/output/part1/part-00000

hdfs dfs -rm -r /user/root/output/part2
hadoop jar /opt/hadoop-3.3.1/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -file /app/jars/mapper2.py -mapper "python3 mapper2.py" -file /app/jars/reducer2.py -reducer "python3 reducer2.py" -input /user/root/input/dataset.csv -output /user/root/output/part2
hdfs dfs -cat /user/root/output/part2/part-00000

hdfs dfs -rm -r /user/root/output/part3
hadoop jar /opt/hadoop-3.3.1/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -file /app/jars/mapper3.py -mapper "python3 mapper3.py" -file /app/jars/reducer3.py -reducer "python3 reducer3.py" -input /user/root/input/dataset.csv -output /user/root/output/part3
hdfs dfs -cat /user/root/output/part3/part-00000

