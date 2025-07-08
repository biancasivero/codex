import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from agents.helloworld.agent_executor import HelloWorldAgentExecutor

class DummyQueue:
    def __init__(self):
        self.events = []
    def enqueue_event(self, event):
        self.events.append(event)

class DummyInput:
    def __init__(self, text: str):
        self.content = text.encode('utf-8')

class DummyContext:
    def __init__(self, text: str):
        self.input = DummyInput(text)

def test_convert_currency_usd_to_brl():
    executor = HelloWorldAgentExecutor()
    queue = DummyQueue()
    ctx = DummyContext("convert 25 USD to BRL")
    import asyncio
    asyncio.run(executor.convert_currency(ctx, queue))
    assert queue.events, "No event enqueued"
    text = queue.events[0].parts[0].root.text
    assert "USD é equivalente" in text
