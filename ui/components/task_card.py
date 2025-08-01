import json

import mesop as me
import pandas as pd

from state.state import ContentPart, SessionTask, StateTask, AppState


def message_string(content: ContentPart) -> str:
    if isinstance(content, str):
        return content
    return json.dumps(content)


def clear_task_history():
    """Clear all tasks from the task list"""
    state = me.state(AppState)
    state.task_list = []
    print("🗑️ Histórico de tarefas limpo!")


@me.component
def task_card(tasks: list[SessionTask]):
    """Task card component"""
    columns = ['Conversation ID', 'Task ID', 'Description', 'Status', 'Output']
    df_data: dict[str, list[str]] = dict([(c, []) for c in columns])
    for task in tasks:
        df_data['Conversation ID'].append(task.context_id)
        df_data['Task ID'].append(task.task.task_id or '')
        df_data['Description'].append(
            '\n'.join(message_string(x[0]) for x in task.task.message.content)
        )
        df_data['Status'].append(task.task.state)
        df_data['Output'].append(flatten_artifacts(task.task))
    df = pd.DataFrame(pd.DataFrame(df_data), columns=columns)
    
    # Header com botão de limpar
    with me.box(
        style=me.Style(
            display='flex',
            justify_content='space-between',
            align_items='center',
            margin=me.Margin.all(16),
            padding=me.Padding.all(8),
            background='#f5f5f5',
            border_radius=8
        )
    ):
        me.text(
            f"📋 Total de tarefas: {len(tasks)}",
            style=me.Style(
                font_weight='bold',
                font_size=16
            )
        )
        me.button(
            "🗑️ Limpar Histórico",
            on_click=clear_task_history,
            type="stroked",
            style=me.Style(
                background='#ff4444',
                color='white',
                border_radius=4,
                padding=me.Padding.symmetric(horizontal=16, vertical=8)
            )
        )
    
    # Tabela de tarefas
    with me.box(
        style=me.Style(
            display='flex',
            justify_content='space-between',
        )
    ):
        if len(tasks) > 0:
            me.table(
                df,
                header=me.TableHeader(sticky=True),
                columns=dict([(c, me.TableColumn(sticky=True)) for c in columns]),
            )
        else:
            me.text(
                "🎉 Nenhuma tarefa no histórico. Use o Marvin para extrair contatos!",
                style=me.Style(
                    text_align='center',
                    font_size=16,
                    color='#666',
                    margin=me.Margin.all(32)
                )
            )


def flatten_artifacts(task: StateTask) -> str:
    parts = []
    for a in task.artifacts:
        for p in a:
            if p[1] == 'text/plain' or p[1] == 'application/json':
                parts.append(message_string(p[0]))
            else:
                parts.append(p[1])

    return '\n'.join(parts)
