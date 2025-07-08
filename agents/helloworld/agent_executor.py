from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
import httpx
import re

class HelloWorldAgentExecutor(AgentExecutor):
    async def hello_world(self, context: RequestContext, event_queue: EventQueue) -> None:
        event_queue.enqueue_event(new_agent_text_message("Hello World"))

    async def super_hello_world(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        event_queue.enqueue_event(new_agent_text_message("Hello World"))

    async def convert_currency(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Extrair o texto da invocação
        input_text = context.input.content.decode("utf-8")

        # Usar regex para extrair valor, moeda de origem e moeda de destino
        # Ex: "convert 10 USD to EUR" ou "how much is 50 BRL in JPY?"
        match = re.search(r'(\d+(\.\d+)?)\s*([a-zA-Z]{3})\s*(?:to|in)\s*([a-zA-Z]{3})', input_text, re.IGNORECASE)

        if not match:
            event_queue.enqueue_event(new_agent_text_message(
                "Não consegui entender o formato da sua solicitação de conversão. Por favor, use o formato 'converter [valor] [moeda_origem] para [moeda_destino]'."
            ))
            return

        amount = float(match.group(1))
        from_currency = match.group(3).upper()
        to_currency = match.group(4).upper()

        try:
            # Para demonstração sem chave API, vamos simular uma taxa de câmbio fixa
            if from_currency == "USD" and to_currency == "BRL":
                converted_amount = amount * 5.00 # Exemplo de taxa
                event_queue.enqueue_event(new_agent_text_message(
                    f"{amount} {from_currency} é equivalente a {converted_amount:.2f} {to_currency} (taxa simulada)."
                ))
            elif from_currency == "BRL" and to_currency == "USD":
                converted_amount = amount / 5.00 # Exemplo de taxa
                event_queue.enqueue_event(new_agent_text_message(
                    f"{amount} {from_currency} é equivalente a {converted_amount:.2f} {to_currency} (taxa simulada)."
                ))
            else:
                event_queue.enqueue_event(new_agent_text_message(
                    f"Conversão de {from_currency} para {to_currency} não suportada na demonstração. Tente USD para BRL ou BRL para USD."
                ))

        except httpx.RequestError as e:
            event_queue.enqueue_event(new_agent_text_message(
                f"Erro de conexão ao tentar converter moedas: {e}"
            ))
        except Exception as e:
            event_queue.enqueue_event(new_agent_text_message(
                f"Ocorreu um erro inesperado durante a conversão: {e}"
            ))

    async def find_and_greet_agent(self, context: RequestContext, event_queue: EventQueue) -> None:
        from .mcp import client as mcp_client
        from a2a.client import A2AClient

        # Find agents using the MCP client
        agents = await mcp_client.find_agents("hello world")
        if not agents:
            event_queue.enqueue_event(new_agent_text_message("No agents found."))
            return

        # Greet each agent
        for agent in agents:
            client = A2AClient(agent_card=agent)
            async with client.connect() as connection:
                response = await connection.execute_skill("hello_world")
                event_queue.enqueue_event(new_agent_text_message(f"Agent {agent.name} responded: {response}"))

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Implementação básica para o método execute
        pass

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Implementação básica para o método cancel
        pass


