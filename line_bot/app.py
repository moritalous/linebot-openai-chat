import os
import json

from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

from linebot.v3 import (WebhookHandler)
from linebot.v3.exceptions import (InvalidSignatureError)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (MessageEvent,TextMessageContent)


LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
NUM_OF_HISTORY = os.getenv('NUM_OF_HISTORY', 10)
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo')
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

line_configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(channel_secret=LINE_CHANNEL_SECRET)

llm = ChatOpenAI(temperature=0, model_name=OPENAI_MODEL_NAME)


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):

    print(event)

    user_id = event.source.user_id
    text = event.message.text

    response = conversation(input=text, session_id=user_id)

    with ApiClient(line_configuration) as api_client:

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=response)]
                )
            )


def conversation(input: str, session_id: str, num_of_history: int = NUM_OF_HISTORY):

    message_history = DynamoDBChatMessageHistory(
    table_name=DYNAMODB_TABLE_NAME, 
    session_id=session_id, 
    )

    memory = ConversationBufferWindowMemory(
        memory_key='history', 
        chat_memory=message_history, 
        return_messages=True,
        k=num_of_history
    )


    conversation = ConversationChain(
        llm=llm, 
        verbose=True, 
        memory=memory
    )

    return conversation.predict(input=input)


def lambda_handler(event, context):

    print(event)

    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    line_handler.handle(body,signature)

    return {
        'statusCode': 200, 
        'body': 'OK'
        }

