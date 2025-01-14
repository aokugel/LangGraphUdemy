from collections import defaultdict
import json
from dotenv import load_dotenv
from typing import List

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolInvocation, ToolExecutor

from schemas import AnswerQuestion, Reflection
from chains import parser

load_dotenv()

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, mex_results=5)
tool_executor = ToolExecutor([tavily_tool])

def execute_tools(state: List[BaseMessage]) -> List[ToolMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)

    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(ToolInvocation(
                tool="tavily_search_results_json",
                tool_input=query
                )
            )
            ids.append(parsed_call["id"])
    outputs = tool_executor.batch(tool_invocations)
    

    outputs_map = defaultdict(dict)

    for id_, output, invocations in zip(ids, outputs, tool_invocations):
        outputs_map[id_][invocations.tool_input] = output

    # convert the mapped outputs to toolmessage objects
    tool_messages = []
    for id_, mapped_output in outputs_map.items():
        tool_messages.append(ToolMessage(content=json.dumps(mapped_output), tool_call_id=id_))

    return tool_messages






if __name__ == "__main__":
    print("who dey")

    human_message = HumanMessage(
        content="Write about AI-Powered SOC / automous soc problem domain,"
        " list startups that do that and raised capital."
    )

    answer = AnswerQuestion(
        answer="",
        reflection=Reflection(missing="", superfluous=""),
        search_queries=[
            "AI-powered SOC startups funding",
            "AI SOC problem domain specifics",
            "Technologies used by AI-powered SOC startups",
        ],
        id="call_KpYHichFFEmLitHFvFhKy1Ra",

    )
    raw_res = execute_tools(
        state=[
            human_message,
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": AnswerQuestion.__name__,
                        "args": answer.model_dump(),
                        "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
                    }
                ],
            ),
        ]
    )
    print(raw_res)
