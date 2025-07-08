from a2a.executor import AgentExecutor
from a2a.types import AgentSkillInvoke, AgentSkillOutput, MediaTypes

class HelloWorldAgentExecutor(AgentExecutor):
    """Simple executor exposing a couple of demo skills."""

    async def hello_world(self, skill_invoke: AgentSkillInvoke) -> AgentSkillOutput:
        """Return a plain ``Hello World`` response."""
        return AgentSkillOutput(output=MediaTypes.TEXT_PLAIN.create_content("Hello World"))

    async def super_hello_world(self, skill_invoke: AgentSkillInvoke) -> AgentSkillOutput:
        """Return an enthusiastic ``Hello World`` response."""
        return AgentSkillOutput(output=MediaTypes.TEXT_PLAIN.create_content("Hello World"))
