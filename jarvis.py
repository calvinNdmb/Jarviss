import os
import time
import wave
import pyaudio
import requests
import operator
import webbrowser
from langchain import hub
from langchain.tools import StructuredTool
from langchain_core.agents import AgentFinish
from typing import Annotated, TypedDict, Union
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph, START
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt.tool_executor import ToolExecutor
from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentAction, AgentFinish


os.environ["OPENAI_API_KEY"] = "sk-gqSDvacX_H8RPXnkauNLBe141Cr8Xt_dsOnCEOxcGZT3BlbkFJzzF7AwF9d8o1E7XNxcAaQP4gKjxjFEVdeGmHhT_AcA"
os.environ["TAVILY_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"

def google_search(search_query = ""):

    if search_query == "":
        open_google()
        return
    url = f"https://www.google.com/search?q={search_query}"

    webbrowser.open(url)
def open_google():
    webbrowser.open("https://www.google.com")
def open_youtube():
    webbrowser.open("https://www.youtube.com")
def youtube_search(search_query = ""):
    if search_query == "":
        open_youtube()
        return
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(url)
def open_github():
    webbrowser.open("https://www.github.com")
def open_chatgpt():
    webbrowser.open("https://chatgpt.com/")
    
def hue():
    IP_address = "192.168.1.21"
    print("Hue!")
    
open_chatgpt_tool = StructuredTool.from_function(func=open_chatgpt, name="open_chatgpt", description="Open ChatGPT website (Dont take arguments)")
open_google_tool = StructuredTool.from_function(func=open_google, name="open_google", description="Open Google website (Dont take arguments)")
open_youtube_tool = StructuredTool.from_function(func=open_youtube, name="open_youtube", description="Open Youtube website (Dont take arguments)")
open_github_tool = StructuredTool.from_function(func=open_github, name="open_github", description="Open Github website (Dont take arguments)")
youtube_search_tool = StructuredTool.from_function(func=youtube_search, name="youtube_search", description="Search on Youtube (Takes search_query as argument)")
google_search_tool = StructuredTool.from_function(func=google_search, name="google_search", description="Search on Google (Takes search_query as argument)")

tools = [open_chatgpt_tool, open_google_tool, open_youtube_tool, open_github_tool, youtube_search_tool, google_search_tool] 

prompt = hub.pull("hwchase17/openai-functions-agent")

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", streaming=True)

agent_runnable = create_openai_functions_agent(llm, tools, prompt)

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

tool_executor = ToolExecutor(tools)

def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}

def execute_tools(data):
    # Get the most recent agent_outcome - this is the key added in the `agent` above
    agent_action = data["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}

def should_continue(data):
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    else:
        return "continue"

def capture_audio(name):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    sound_file = wave.open(f"{name}.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)

    print("Enregistrement... Appuyez sur 'f12' pour arrêter.")
    start_time = time.time()
    
    while True:
        sound_file.writeframes(stream.read(1024))
        if keyboard.is_pressed('f12') or (time.time() - start_time > 30):
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()
    sound_file.close()
    
    return f"{name}.wav"

def req_whisper(audio_file_path, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {'file': open(audio_file_path, 'rb'), 'model': (None, 'whisper-1')}
    response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, files=files)

    if response.status_code == 200:
        return "Transcription:", response.json()['text']
    return f"Erreur : {response.status_code} - {response.text}"

workflow = StateGraph(AgentState)
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")
app = workflow.compile()


def interact_w_jarvis(request):
    inputs = {"input": str(request), "chat_history": []}
    last_message = None
    for s in app.stream(inputs):
        last_message = list(s.values())[0]  # Garde en mémoire seulement le dernier message
    return last_message 