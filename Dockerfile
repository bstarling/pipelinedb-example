FROM postgres:10.6

RUN apt-get update \
     && apt-get install -y --no-install-recommends \
     # there must be a better way
        curl \
        git \ 
        ca-certificates \
        build-essential \
        libssl-dev \
        libz-dev \
    # required to build pipeline_kafka from source
        postgresql-server-dev-10 \ 
    # makes testing easier
        kafkacat


RUN curl -s http://download.pipelinedb.com/apt.sh | bash \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
     # What we actually need
        pipelinedb-postgresql-10

RUN git clone -b v0.11.6 http://github.com/edenhill/librdkafka.git ~/librdkafka \
    && cd ~/librdkafka && ./configure --prefix=/usr --disable-ssl && make && make install
    
RUN git clone http://github.com/pipelinedb/pipeline_kafka.git ~/pipeline_kafka \
    && cd ~/pipeline_kafka && ./configure && make && make install


COPY ./config/postgresql.conf /etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]
