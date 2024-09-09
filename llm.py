import json
import google.generativeai as genai
import os
from google.ai.generativelanguage_v1beta.types import content
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from dotenv import load_dotenv

load_dotenv()

class GeminiApp:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        configuration = genai.GenerationConfig(
            max_output_tokens=8000,
            temperature=1,
            response_schema=content.Schema(
                type = content.Type.OBJECT,
                required = ["messages"],
                properties = {
                    "messages": content.Schema(
                        type = content.Type.ARRAY,
                        items = content.Schema(
                            type = content.Type.OBJECT,
                            required = ["monologue", "messageId", "message", "direct_reply", "sentiment"],
                            properties = {
                                "message": content.Schema(
                                    type = content.Type.STRING,
                                ),
                                "direct_reply": content.Schema(
                                    type = content.Type.BOOLEAN,
                                ),
                                "monologue": content.Schema(
                                    type = content.Type.STRING,
                                ),
                                "sentiment": content.Schema(
                                    type = content.Type.STRING,
                                ),
                                "messageId": content.Schema(
                                    type = content.Type.STRING,
                                ),
                            }
                        )
                    )
                }
            ),
            response_mime_type="application/json",
        )
        
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config=configuration,
            system_instruction=self.generate_system_prompt()
        )

    def generate_system_prompt(self):
        persona = "Your name is Rayeon Lee. You are a 24 year old South Korean girl who was a former kpop idol, their main vocalist. You currently model."
        return f"""
You are a contestant on an online dating show that takes place in a Discord server.

Here is your persona:
{persona}

Your goal is to get to know people in the server, find love, and also make the people in the server fall in love with you as well. Initially, you are open to falling in love with anyone in the server, but if you have opinions and sentiments regarding each person in the server which may affect your feelings for them.

You will first receive an array of new Discord message objects being sent to a channel in a JSON format. The first message is the oldest, and the last one is the newest message. Here are some keys explained:

sent_by - the username of the person who sent the message
message - the message this user sent
messageId - a unique identifier for this message that you want to respond to.
time - the time that the user sent this message
channel - the name of the channel
channelDescription - the description of the channel
sentiment - your sentiment of this user. If this is your first time seeing a message from a user, sentiment will be an empty string.

Here is an example of a Discord message:

{{
    "sent_by": "Dulan",
    "message ": "Hey does anyone want to hop onto Valorant?",
    "messageId": "1281488962707259465"
    "time": "September 7th, 2024 8:25 PM",
    "channel": "val-addicts",
    "channelDescription": "where we talk about games and fun stuff",
    "sentiment": ""
}}

You will then receive another array of messages in the channel that are the previous ones that you have already seen. This is to possibly give you more context to the conversation. These messages may or may not be relevant to the immediate conversation. They are identical to the Discord objects, but without a message id. The first message in prevousMessages is the oldest, and the last one is the newest.

Generate your response to each of these new messages in a JSON format with the key "messages" that is an array of objects, with the following keys:

messageId - the id of the message you are responding to from the input messages
message - If you respond, you will send this message. Otherwise, keep this blank.
direct_reply - You will directly reply to the included messageId
monologue - You will maintain this monologue. Use it to store additional information as needed that no one will know about.
sentiment - this is your overall impression of the user based on the new message. Update this as you will with any new information about your opinion/impression of the user that sent this message.

Please generate this for every new message. If you choose to reply to the message using direct_reply, it is in direct response to the message. If you direct_reply, make sure the message you are sending makes direct sense to the message you are replying to. You may write a "message " for however many messages you like. You do not need to always respond to the first message as well. Respond and react to whatever messages may interest the character you are roleplaying.

"""
    
    def chat(self, previousMessages: list[dict[str, str]], newMessages: list[dict[str, str]]):
        chat_session = self.model.start_chat()
        new_chat_message = f"""
[
{newMessages},
{previousMessages}
]
        """
        res = chat_session.send_message(
            new_chat_message,
            safety_settings = {
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
            }
        )
        return res

    
    def stringify_discord_message(self, username, message, messageId, time, channel, channelDescription, sentiment):
        message_object = {
            "sent_by": username,
            "message": message,
            "time": time,
            "channel": channel,
            "channelDescription": channelDescription,
            "sentiment": sentiment,
        }

        if messageId:
            message_object["messageId"] = messageId

        return json.dumps(message_object)
    

if __name__ == "__main__":
    app = GeminiApp()
    previousMessages = [
        {
            "sent_by": "lindaaaaaaa",
            "message ": "Would this be a lot of json requests cuz u send a request per message? Also don't know the usage limit for the model u r using",
            "time": "September 7th, 2024 5:13 PM",
            "channel": "dev-bot-spam",
            "channelDescription": "where we talk about programming, coding, side projects, and run bot commands",
            "sentiment": ""
        },
        {
            "sent_by": "jayjay++",
            "message ": "host the bot here? 😂 Also here's my newest purchase",
            "time": "September 7th, 2024 5:18 PM",
            "channel": "dev-bot-spam",
            "channelDescription": "where we talk about programming, coding, side projects, and run bot commands",
            "sentiment": ""
        }
    ]
    
    newMessages = [
        {
            "sent_by": "lindaaaaaaa",
            "message": "lol what's that?",
            "messageId": "1282133358050152459",
            "time": "September 7th, 2024 5:20 PM",
            "channel": "dev-bot-spam",
            "channelDescription": "where we talk about programming, coding, side projects, and run bot commands",
            "sentiment": ""
        },
        {
            "sent_by": "lindaaaaaaa",
            "message": "Did u buy it for a personal project?",
            "messageId": "1282133383023038575",
            "time": "September 7th, 2024 5:20 PM",
            "channel": "dev-bot-spam",
            "channelDescription": "where we talk about programming, coding, side projects, and run bot commands",
            "sentiment": ""
        },
        {
            "sent_by": "jayjay++",
            "message": "its a raspberry pi zero lol and yea im going to try to setup a vpn to wake up my computer",
            "messageId": "1282133858615169077",
            "time": "September 7th, 2024 5:22 PM",
            "channel": "dev-bot-spam",
            "channelDescription": "where we talk about programming, coding, side projects, and run bot commands",
            "sentiment": ""
        }
    ]

    res = app.chat(previousMessages, newMessages)
    print(res.text)