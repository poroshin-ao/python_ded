from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

class Is_lower(ABCRule[Message]):
    def __init__(self, text: str):
        self.text = text.lower()

    async def check(self, event: Message) -> bool:
        return event.text.lower() == self.text