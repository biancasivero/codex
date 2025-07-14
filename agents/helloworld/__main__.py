import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import HelloWorldAgentExecutor

# --8<-- [start:AgentSkill]
skill = AgentSkill(
    id="hello_world",
    name="Intelligent Hello World",
    description="Provides contextual hello world responses based on user input. Detects intent and responds accordingly with basic, standard, or super greetings.",
    tags=["hello world", "greeting", "intelligent", "contextual"],
    examples=[
        "hi", 
        "hello world", 
        "super hello", 
        "amazing hello", 
        "simple hello",
        "basic greeting",
        "awesome hello"
    ],
)
# --8<-- [end:AgentSkill]
# --8<-- [start:AgentCard]
# This will be the public-facing agent card
public_agent_card = AgentCard(
    name="Hello World Agent",
    description="Intelligent hello world agent that provides contextual responses",
    url="http://localhost:9999/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],
)
# --8<-- [end:AgentCard]
request_handler = DefaultRequestHandler(
    agent_executor=HelloWorldAgentExecutor(),
    task_store=InMemoryTaskStore(),
)
server = A2AStarletteApplication(
    agent_card=public_agent_card,
    http_handler=request_handler,
)

app = server.build()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9999)


