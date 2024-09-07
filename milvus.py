import json
from pymilvus import CollectionSchema, DataType, FieldSchema, MilvusClient
import os
from dotenv import load_dotenv

load_dotenv()

class MilvusApp:
	def __init__(self):
		self.client = MilvusClient(
			uri=os.getenv("ZILLIZ_PUBLIC_ENDPOINT"),
			token=os.getenv("ZILLIZ_API_KEY")
		)

	def disconnect(self):
		if self.client:	
			self.client.close()

	def create_chat_schema(self) -> CollectionSchema:
		embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768, description="Vectorized chat message")
		message_field = FieldSchema(name="message", dtype=DataType.VARCHAR, max_length=2000, description="Original chat message")
		user_id_field = FieldSchema(name="user_id", dtype=DataType.VARCHAR, max_length=64, description="ID of the user")
		timestamp_field = FieldSchema(name="timestamp", dtype=DataType.INT64, description="Timestamp of the message")
		message_id_field = FieldSchema(name="message_id", dtype=DataType.VARCHAR, max_length=64, description="Unique ID of the message", is_primary=True, auto_id=True)
		channel_id_field = FieldSchema(name="channel_id", dtype=DataType.VARCHAR, max_length=64, description="ID of the conversation or channel")

		schema = CollectionSchema(
			fields=[embedding_field, message_field, user_id_field, timestamp_field, message_id_field, channel_id_field],
			description="Discord Chat logs collection"
		)

		return schema
	
	def create_persona_schema(self) -> CollectionSchema:

		# TODO: consider instead of individual lines of dialogue, consider an entire scene or conversation?

		embedding_field = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768, description="Vectorized show dialogue")
		dialogue_field = FieldSchema(name="dialogue", dtype=DataType.VARCHAR, max_length=1000, description="Original show dialogue")
		character_field = FieldSchema(name="character", dtype=DataType.VARCHAR, max_length=100, description="Character name")
		scene_context_field = FieldSchema(name="scene_context", dtype=DataType.VARCHAR, max_length=1000, description="Description of the scene or context")
		dialogue_id_field = FieldSchema(name="dialogue_id", dtype=DataType.VARCHAR, max_length=64, description="Unique ID of the dialogue", is_primary=True, auto_id=True)

		schema = CollectionSchema(
			fields=[embedding_field, dialogue_field, character_field, scene_context_field, dialogue_id_field],
			description="Collection for show dialogue"
		)

		return schema

	def create_collection(self, collection_name: str, field_name: str, schema: CollectionSchema):
		res = self.client.list_collections()
		if collection_name in res:
			raise Exception(f"'{collection_name}' already exists in cluster.\n{self.client.describe_collection(collection_name=collection_name)}")
		index_params = self.client.prepare_index_params()
        
		index_params.add_index(
			field_name=field_name, 
			index_type="AUTOINDEX", # zilliz
			metric_type="L2",
			params={}
		)

		collection = self.client.create_collection(
			collection_name=collection_name,
			schema=schema,
			index_params=index_params
		)
		return collection
	
	def load_collection(self, collection_name: str) -> None:
		self.client.get_collection(collection_name=collection_name)
	
		res = self.client.get_load_state(
			collection_name=collection_name
		)

		print(res)

	def drop_collection(self, collection_name: str):
		self.client.drop_collection(collection_name=collection_name)

	def upload_data(self, collection_name: str, data):
		self.client.insert(collection_name=collection_name, data=data)

	def find_data(self, collection_name: str, query_vectors: list, top_k=5):
		self.load_collection(collection_name)
		res = self.client.search(
			collection_name=collection_name,
			data=query_vectors,
			limit=top_k, # Max. number of search results to return
			search_params={"metric_type": "L2"}
		)

if __name__ == "__main__":
	print("Connecting to Milvus")
	app = MilvusApp()
	print("Creating chat schema")
	chat_schema = app.create_chat_schema()
	print("Creating persona schema")
	persona_schema = app.create_persona_schema()

	print("Creating discord chat logs collection")
	chat_collection = app.create_collection("discord_chat_logs", "embedding", chat_schema)
	print("Creating show dialogue collection")
	persona_collection = app.create_collection("show_dialogue", "embedding", persona_schema)

	print("Dropping discord chat logs collection")
	app.drop_collection("discord_chat_logs")
	print("Dropping show dialogue collection")
	app.drop_collection("show_dialogue")

	print("Disconnecting from Milvus")
	app.disconnect()
	print("Finished testing Milvus")