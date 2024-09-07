from pymilvus import CollectionSchema, DataType, FieldSchema, connections, MilvusClient
import os
from dotenv import load_dotenv

load_dotenv()

class MilvusApp:
	def __init__(self):
		self.client = connections.connect(
			uri=os.getenv("ZILLIZ_PUBLIC_ENDPOINT"),
			token=os.getenv("ZILLIZ_API_KEY")
		)

	def disconnect(self):
		if self.client:	
			self.client.close()

	def create_schema():
		embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768, description="Vectorized chat message")
		message_field = FieldSchema(name="message", dtype=DataType.VARCHAR, max_length=2000, description="Original chat message")
		user_id_field = FieldSchema(name="user_id", dtype=DataType.VARCHAR, max_length=64, description="ID of the user")
		timestamp_field = FieldSchema(name="timestamp", dtype=DataType.INT64, description="Timestamp of the message")
		message_id_field = FieldSchema(name="message_id", dtype=DataType.VARCHAR, max_length=64, description="Unique ID of the message")
		channel_id_field = FieldSchema(name="channel_id", dtype=DataType.VARCHAR, max_length=64, description="ID of the conversation or channel")

		schema = CollectionSchema(
			fields=[embedding_field, message_field, user_id_field, timestamp_field, message_id_field, channel_id_field],
			description="Discord Chat logs collection"
		)

		return schema
