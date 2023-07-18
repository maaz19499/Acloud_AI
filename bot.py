# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount
from chat_utils import *


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hi Welcome to ACloudz.AI, Your one stop destination for all the services!")

    async def on_message_activity(self, turn_context: TurnContext):
        # await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")
        greeting_list = ['Hi','Hello','HI','hi','Hey','HEY','hey','hello']
        exit_list = ['Bye','bye','exit','quit','goodbye','Goodbye']
        if turn_context.activity.text in greeting_list:
            answer= 'Hello, how can I help you?'
        elif turn_context.activity.text in exit_list:
            answer= 'Bye, have a Good Day!'
        else:
            answer = get_answers(turn_context.activity.text)  
        return await turn_context.send_activity(MessageFactory.text(answer))

    
