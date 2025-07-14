import base64
import logging
import uuid

from collections.abc import AsyncIterable
from io import BytesIO
from typing import Any
from uuid import uuid4

import matplotlib.pyplot as plt
import pandas as pd

from crewai import Agent, Crew, Task
from crewai.process import Process
from crewai.tools import tool
from dotenv import load_dotenv
from pydantic import BaseModel
from utils import cache


load_dotenv()

logger = logging.getLogger(__name__)


class Imagedata(BaseModel):
    id: str | None = None
    name: str | None = None
    mime_type: str | None = None
    bytes: str | None = None
    error: str | None = None


@tool('ChartGenerationTool')
def generate_chart_tool(prompt: str, session_id: str) -> str:
    """Generates a bar chart image from CSV-like input using matplotlib."""
    logger.info(f'>>>Chart tool called with prompt: {prompt}')

    if not prompt:
        raise ValueError('Prompt cannot be empty')

    try:
        # Parse CSV-like input
        from io import StringIO

        df = pd.read_csv(StringIO(prompt))
        if df.shape[1] != 2:
            raise ValueError(
                'Input must have exactly two columns: Category and Value'
            )
        df.columns = ['Category', 'Value']
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        if df['Value'].isnull().any():
            raise ValueError('All values must be numeric')

        # Generate bar chart
        fig, ax = plt.subplots()
        ax.bar(df['Category'], df['Value'])
        ax.set_xlabel('Category')
        ax.set_ylabel('Value')
        ax.set_title('Bar Chart')

        # Save to buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        image_bytes = buf.read()

        # Encode image
        data = Imagedata(
            bytes=base64.b64encode(image_bytes).decode('utf-8'),
            mime_type='image/png',
            name='generated_chart.png',
            id=uuid4().hex,
        )

        logger.info(
            f'Caching image with ID: {data.id} for session: {session_id}'
        )

        # Cache image
        session_data = cache.get(session_id) or {}
        session_data[data.id] = data
        cache.set(session_id, session_data)

        return data.id

    except Exception as e:
        logger.error(f'Error generating chart: {e}')
        return -999999999


class ChartGenerationAgent:
    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain', 'image/png']

    def __init__(self):
        self.chart_creator_agent = Agent(
            role='Chart Creation Expert',
            goal='Generate a bar chart image based on structured CSV input.',
            backstory='You are a data visualization expert who transforms structured data into visual charts.',
            verbose=False,
            allow_delegation=False,
            tools=[generate_chart_tool],
        )

        self.chart_creation_task = Task(
            description=(
                "You are given a prompt: '{user_prompt}'.\n"
                "If the prompt includes comma-separated key:value pairs (e.g. 'a:100, b:200'), "
                "reformat it into CSV with header 'Category,Value'.\n"
                "Ensure it becomes two-column CSV, then pass that to the 'ChartGenerationTool'.\n"
                "Use session ID: '{session_id}' when calling the tool."
            ),
            expected_output='The id of the generated chart image',
            agent=self.chart_creator_agent,
        )

        self.chart_crew = Crew(
            agents=[self.chart_creator_agent],
            tasks=[self.chart_creation_task],
            process=Process.sequential,
            verbose=False,
        )

    import uuid

    def invoke(self, query, session_id: str | None = None) -> str:
        # Normalize or generate session_id
        session_id = session_id or f'session-{uuid.uuid4().hex}'
        logger.info(
            f'[invoke] Using session_id: {session_id} for query: {query}'
        )

        try:
            inputs = {
                'user_prompt': query,
                'session_id': session_id,
            }

            response = self.chart_crew.kickoff(inputs)
            logger.info(f'[invoke] Chart crew kickoff response: {response}')
            
            # Verificar se a resposta é válida
            if response is None:
                logger.error('[invoke] Chart crew returned None')
                raise ValueError('Chart crew returned None')
            
            # Criar um objeto de resultado mock se necessário
            class MockResult:
                def __init__(self, raw_value):
                    self.raw = raw_value
            
            # Se response for uma string, criar um objeto mock
            if isinstance(response, str):
                result = MockResult(response)
            else:
                result = response
            
            logger.info(f'[invoke] Chart tool returned result: {result}')
            return result
            
        except Exception as e:
            logger.error(f'[invoke] Error in chart crew kickoff: {e}')
            # Retornar um resultado de erro
            class ErrorResult:
                def __init__(self, error_msg):
                    self.raw = f'error-{uuid.uuid4().hex}'
                    self.error = error_msg
            
            return ErrorResult(str(e))

    async def stream(self, query: str) -> AsyncIterable[dict[str, Any]]:
        """Streaming implementation for Chart Generator Agent"""
        try:
            # Simulate streaming chunks while processing
            yield {"type": "status", "message": "Starting chart generation..."}
            
            # Generate session ID for streaming
            session_id = f'stream-{uuid.uuid4().hex}'
            
            # Process the query using the crew
            result = self.invoke(query, session_id)
            
            yield {"type": "status", "message": "Chart processing completed"}
            
            # Get the final result
            data = self.get_image_data(session_id=session_id, image_key=result.raw)
            
            if data and not data.error:
                yield {
                    "type": "result", 
                    "data": {
                        "name": data.name,
                        "id": data.id,
                        "success": True
                    }
                }
            else:
                yield {
                    "type": "error", 
                    "message": data.error if data else "Failed to generate chart"
                }
                
        except Exception as e:
            logger.error(f"Error in stream method: {e}")
            yield {"type": "error", "message": str(e)}

    def get_image_data(self, session_id: str, image_key: str) -> Imagedata:
        session_data = cache.get(session_id)

        if not session_data:
            logger.error(
                f'[get_image_data] No session data for session_id: {session_id}'
            )
            return Imagedata(
                error=f'No session data found for session_id: {session_id}'
            )

        if image_key not in session_data:
            logger.error(
                f'[get_image_data] Image key {image_key} not found in session data'
            )
            return Imagedata(
                error=f'Image ID {image_key} not found in session {session_id}'
            )

        return session_data[image_key]

    async def process_request(self, query: str, session_id: str, skill: str = None) -> dict[str, Any]:
        """Process a chart generation request following HelloWorld Agent pattern."""
        try:
            logger.info(f"Processing chart generation request: {query} (session: {session_id})")
            
            # Usar o método invoke existente
            result = self.invoke(query, session_id)
            
            # Verificar se houve erro
            if hasattr(result, 'error') and result.error:
                return {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "result": f"Chart generation failed: {result.error}",
                    "success": False
                }
            
            # Verificar se o resultado é válido
            if result and hasattr(result, 'raw'):
                # Tentar obter os dados da imagem
                data = self.get_image_data(session_id=session_id, image_key=result.raw)
                
                if data and not data.error:
                    return {
                        "is_task_complete": True,
                        "require_user_input": False,
                        "result": f"Chart generated successfully: {data.name}",
                        "chart_id": data.id,
                        "chart_name": data.name,
                        "success": True
                    }
                else:
                    error_msg = data.error if data else "Failed to generate chart image"
                    return {
                        "is_task_complete": True,  # Marca como completo mesmo com erro
                        "require_user_input": False,
                        "result": f"Chart generation error: {error_msg}",
                        "success": False
                    }
            else:
                return {
                    "is_task_complete": True,  # Marca como completo mesmo com erro
                    "require_user_input": False,
                    "result": "Chart generation failed: Invalid result from crew",
                    "success": False
                }
                
        except Exception as e:
            logger.exception(f"Error in chart generation for session {session_id}")
            return {
                "is_task_complete": True,  # Sempre completa, mesmo com erro
                "require_user_input": False,
                "result": f"Chart generation error: {str(e)}",
                "success": False
            }
