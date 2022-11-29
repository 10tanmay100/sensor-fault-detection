from Sensor.configuration.mongodb_connection import MongoDBClient
from Sensor.logger import logging


if __name__ == '__main__':
    logging.info("Connecting to mongodb...")
    mongodb_client=MongoDBClient()
    print(mongodb_client.database.list_collection_names())

