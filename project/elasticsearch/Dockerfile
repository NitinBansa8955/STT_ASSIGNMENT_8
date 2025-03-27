# Using official Elasticsearch image from Elastic's registry and Specifying version 7.17.0 for compatibility

FROM docker.elastic.co/elasticsearch/elasticsearch:7.17.0


# Copying custom configuration file into container
COPY config/elasticsearch.yml /usr/share/elasticsearch/config/

RUN mkdir /data && chown -R elasticsearch:elasticsearch /data

# Defining persistent storage volume
VOLUME /data

USER elasticsearch

# Starting the Elasticsearch with custom data path
CMD ["elasticsearch", "-Epath.data=/data"]