import os

import flet as ft
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel
from langgraph.checkpoint.memory import  InMemorySaver

# from dotenv import load_dotenv
# load_dotenv()
# print(os.getenv("OPENAI_API_BASE"))

class CapitalInfo(BaseModel):
    name:str
    location:str
    vibe:str
    economy:str


@tool(description="获取给定城市的天气")
def getWeather(location: str) -> str:
    return f"{location} 是大晴天哦"

@tool
def suare_root(x: float):
    """
    Calculate the square root of a number
    Args:
        x (float): The number to calculate the square root of
    """
    return x ** 0.5

llm = init_chat_model(
    model="GLM-5V-Turbo",
    model_provider="openai",
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    api_key="98a5a30a82e04e45b5539081929135c1.vRNj0WIQeg9j7rXT",
)

agent = create_agent(model=llm,tools=[getWeather],
                     system_prompt="你是一个科幻作家，根据用户的要求创建一个太空之都。",
                     checkpointer=InMemorySaver(),
                     )

config={"configurable":{"thread_id":"thread_1"}}
message = [HumanMessage(content="月球的首都是什么")]

response=agent.invoke({"messages":message}, config=config)

print(response)


async def main(page: ft.Page):
    page.title = "RawImage photo viewer"


    page.add(
        ft.Row(
            [
                ft.Text(response)

            ],
            spacing=10,
        ),

    )



if __name__ == "__main__":
    ft.run(main)