import psycopg2

conn_string = "host='localhost' dbname='pipeline' user='pipeline' password='changeme' port='15432'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

# db setup
setup_sql = """
CREATE extension IF NOT EXISTS pipelinedb;
CREATE extension IF NOT EXISTS pipeline_kafka;
"""
cursor.execute(setup_sql)
conn.commit()

cursor.execute("SELECT pipeline_kafka.add_broker('kafka:9092')")
conn.commit()


# create purchase stream table
create_stream = """
CREATE foreign TABLE IF NOT EXISTS purchase_stream (payload JSON)
SERVER pipelinedb
"""

cursor.execute(create_stream)
conn.commit()

# Count purchases
message_count_view = """
CREATE view purchase_count AS SELECT count(*) from purchase_stream
"""

cursor.execute(message_count_view)
conn.commit()


create_sum_view ="""
CREATE VIEW purchase_summary as select payload->>'category' as category,
sum(CAST(payload->>'price' as FLOAT)) as gross_sales,
sum(CAST(payload->>'tax' as FLOAT)) as sales_tax
FROM purchase_stream group by category
"""

cursor.execute(create_sum_view)
conn.commit()


create_avg_view="""
CREATE VIEW purchase_average as select payload->>'category' as category,
avg(CAST(payload->>'price' as FLOAT)) as avg_sale
FROM purchase_stream group by category
"""

cursor.execute(create_avg_view)
conn.commit()
