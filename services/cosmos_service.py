import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

COSMOS_CONNECTION_STRING = os.getenv("COSMOS_CONNECTION_STRING")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STRING)

database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)