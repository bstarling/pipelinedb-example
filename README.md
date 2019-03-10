# Pipelinedb Docker Demo
This repo contains all the code/configuration needed to create a working postgresql database + [pipelinedb](https://www.pipelinedb.com/) postgresql extension + kafka_pipeline integration in a docker environment. Pipeline kafka integration must be compiled from source and most of the documentation / blog posts are out of date. This repo will show you how to get a working environment. 

### Quick start
This repo is built to get a minimum pipelinedb + kafka plugin working so you can start to experiment on your own.

To start it up run
```
./run-demo.sh
```

There are several scripts contained in this repo to help you populate the required tables and generate test data so you can see pipelinedb in action.

#### Prerequisites
Create a python virtualenv (tested with python `version 3.7.1`) and install the required dependences found `/scripts/requirements.txt`. You can do this from docker as well if you prefer.

In order to run the post from your local and post messages to the docker kafka cluster you will need to add `127.0.0.0    kafka` to your `/etc/hosts` file. 

#### Database Setup
```
python scripts/db_setup.py
```

Login to the database now (default PW is `changeme`)

```
psql -U pipeline -p 15432 -h localhost
```

Check the internal pipeline_kafka tables with `\dt pipeline_kafka.*`
```
pipeline=# \dt pipeline_kafka.*
               List of relations
     Schema     |   Name    | Type  |  Owner
----------------+-----------+-------+----------
 pipeline_kafka | brokers   | table | pipeline
 pipeline_kafka | consumers | table | pipeline
 pipeline_kafka | offsets   | table | pipeline
(3 rows)
```

See the summary tables that have been created `\dt`

```
pipeline=# \dt
                 List of relations
 Schema |         Name          | Type  |  Owner
--------+-----------------------+-------+----------
 public | purchase_average_mrel | table | pipeline
 public | purchase_count_mrel   | table | pipeline
 public | purchase_summary_mrel | table | pipeline
(3 rows)
```

#### Add sample data
These will be empty until we generate some data

Generate your first batch of data
```
python scripts/generate_data.py
```
This script will create a random purchase json message and post it to kafka.

To start the kafka consumer, run this command (must have created the topic first)
```
SELECT pipeline_kafka.consume_begin('purchase_stream_topic', 'purchase_stream',
format :='json', start_offset:=0);
```

#### View Results
You can query your summary tables and see results populated.

Drip data in slowly by changing the `pause` parameter in the `generate_data.py` script to see it changing in real time.

```
pipeline=# select * from purchase_count;
 count
-------
  1000
(1 row)

pipeline=# select * from purchase_summary;
  category   | gross_sales | sales_tax
-------------+-------------+-----------
 coffee      |      2547.5 |    216.48
 baked_goods |     2602.95 |    221.29
(2 rows)

pipeline=# select * from purchase_average;
  category   | avg_sale
-------------+----------
 coffee      |    5.095
 baked_goods |   5.2059
(2 rows)
```

### Resources
* [Pipelinedb 1.0.0](http://docs.pipelinedb.com/)
* [Pipeline Kafka](http://docs.pipelinedb.com/integrations.html)
* [SQL on KAFKA](https://www.pipelinedb.com/blog/sql-on-kafka) Warning:Synxax has changed since this was published!
* [Postgres Docker image](https://hub.docker.com/_/postgres/)
