import os
from groq import Groq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any, Optional, Annotated, Literal
import json
import wikipedia

# Try to import Tavily, with fallback for web search
try:
    from tavily import TavilyClient
    TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
    have_tavily = bool(TAVILY_API_KEY)
except ImportError:
    have_tavily = False

# Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


# Define the state for our graph
class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    search_results: Optional[str]
    network_expertise: Optional[str]
    need_web_search: bool
    need_network_expertise: bool
    final_answer: Optional[str]
    next: Optional[str]


def web_search(query: str) -> str:
    """Perform a web search using available tools"""
    try:
        if have_tavily:
            tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
            search_result = tavily_client.search(query=query,
                                                 search_depth="advanced")
            return json.dumps(search_result, indent=2)
        else:
            try:
                search_results = wikipedia.search(query)
                st.write(f"Got results from Wikipedia{query}")
                if search_results:
                    page = wikipedia.page(search_results[0])
                    return f"Title: {page.title}\nSummary: {wikipedia.summary(search_results[0], sentences=5)}"
                else:
                    return f"No Wikipedia results found for '{query}'"
            except Exception as wiki_error:
                return f"Wikipedia search failed: {str(wiki_error)}"
    except Exception as e:
        return f"Search error: {str(e)}"


def call_groq_model(messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=500):
    """Call Groq model with the provided messages"""
    try:
        completion = client.chat.completions.create(messages=messages,
                                                    model=model,
                                                    temperature=temperature,
                                                    max_tokens=max_tokens)
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error calling Groq API: {str(e)}"


def router(state: AgentState) -> AgentState:
    """Route to the appropriate node based on the state"""
    next_step = None
    if state["need_web_search"]:
        next_step = "search"
    elif state["need_network_expertise"]:
        next_step = "network_expert"
    else:
        next_step = "final"

    return {**state, "next": next_step}


def search_agent(state: AgentState) -> AgentState:
    """Web search agent that looks for information online"""
    messages = state["messages"]
    last_message = messages[-1]["content"] if messages[-1][
        "role"] == "user" else "network troubleshooting"

    search_results = web_search(last_message)

    return {
        **state, "search_results": search_results,
        "need_web_search": False
    }


def network_expert(state: AgentState) -> AgentState:
    """Network troubleshooting expert agent"""
    messages = state["messages"]
    search_results = state.get("search_results", "")

    system_message = """You are a network troubleshooting expert. 
    Provide clear, step-by-step solutions for network-related issues.
    Focus on practical advice and best practices.
    Be concise and to the point.
    Give the user a list of network troubleshooting steps and why they are important."""

    expert_messages = [{"role": "system", "content": system_message}]

    if search_results:
        expert_messages.append({
            "role":
            "system",
            "content":
            f"Here's some relevant information from a web search: {search_results}"
        })

    for message in messages:
        if message["role"] in ["user", "assistant"]:
            expert_messages.append(message)

    expertise = call_groq_model(expert_messages)

    return {
        **state, "network_expertise": expertise,
        "need_network_expertise": False
    }


def final_answer(state: AgentState) -> AgentState:
    """Generate the final answer combining all information"""
    network_expertise = state.get("network_expertise", "")
    search_results = state.get("search_results", "")
    messages = state["messages"]

    system_message = """You are a helpful assistant that provides accurate network troubleshooting advice.
    Use the information provided to give the best answer possible.
    Be concise, clear, and practical."""

    final_messages = [{"role": "system", "content": system_message}]

    context = "Based on the following information:\n"
    if network_expertise:
        context += f"\nNETWORK EXPERT ANALYSIS:\n{network_expertise}\n"
    if search_results:
        context += f"\nRELEVANT SEARCH RESULTS:\n{search_results}\n"

    final_messages.append({"role": "system", "content": context})

    for message in messages:
        if message["role"] in ["user", "assistant"]:
            final_messages.append(message)

    answer = call_groq_model(final_messages)

    return {**state, "final_answer": answer}


def create_agent_graph():
    """Create the LangGraph for the agents"""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router)
    workflow.add_node("search", search_agent)
    workflow.add_node("network_expert", network_expert)
    workflow.add_node("final", final_answer)

    # Set entry point
    workflow.set_entry_point("router")

    # Add conditional edges from router
    workflow.add_conditional_edges("router", lambda x: x["next"], {
        "search": "search",
        "network_expert": "network_expert",
        "final": "final"
    })

    # Add edges to complete the workflow
    workflow.add_edge("search", "network_expert")
    workflow.add_edge("network_expert", "final")
    workflow.add_edge("final", END)

    return workflow.compile()


# Initialize the agent graph
agent_graph = create_agent_graph()


def get_groq_response(prompt: str) -> str:
    """
    Get response from Groq API for network troubleshooting using LangGraph agents
    """
    try:
        # Check if it's a simple greeting
        lower_prompt = prompt.lower().strip()
        if lower_prompt in ["hi", "hello", "hey"]:
            system_message = """You are a network troubleshooting expert. 
            Greet the user warmly and ask them to describe their network issue."""

            completion = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": system_message
                }, {
                    "role": "user",
                    "content": prompt
                }],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=150)

            return completion.choices[0].message.content

        # For network questions, use the agent graph
        state = {
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "search_results": None,
            "network_expertise": None,
            "need_web_search": True,
            "need_network_expertise": True,
            "final_answer": None,
            "next": None
        }

        result = agent_graph.invoke(state)

        if result["final_answer"]:
            return result["final_answer"]
        elif result["network_expertise"]:
            return result["network_expertise"]
        else:
            return "I couldn't find a specific answer. Please try asking your question differently."

    except Exception as e:
        return f"Error: Unable to get response. {str(e)}"
