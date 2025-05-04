import os
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.agents import Tool
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from datetime import datetime
from langchain_openai import ChatOpenAI

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
 
# Initialize the OpenAI language model
llm = ChatOpenAI()
 
# Define the tools the agent can use
tools = []
 
# 1. Example Custom Tool (gets the current time and location)
def get_current_context():
    """Returns the current time and location."""
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    current_location = "Delhi, Delhi, India"  # As per the context
    return f"The current time is {current_time} in {current_location}."


# No API key is typically needed for DuckDuckGoSearchAPIWrapper
 
def create_duckduckgo_search_tool():
    """Creates a Langchain tool for DuckDuckGo Search, incorporating current context."""
    search = DuckDuckGoSearchAPIWrapper()
 
    def search_with_context(query: str) -> str:
        """Performs a DuckDuckGo search, incorporating the current time and location for better relevance."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")
        context_aware_query = f"{query} (current time: {current_time}, location: Delhi, India)"
        print(f"Performing context-aware DuckDuckGo search for: '{context_aware_query}'")
        return search.run(context_aware_query)
 
    duckduckgo_search_tool = Tool(
        name="DuckDuckGo Search",
        func=search_with_context,
        description="useful for when you need to answer questions about current events or general knowledge using the DuckDuckGo search engine. Input should be a search query. This tool is aware of the current time and location for potentially better results.",
    )
    return duckduckgo_search_tool
 

current_context_tool = Tool(
    name="Current Context",
    func=get_current_context,
    description="useful for getting the current time and location.",
)
tools.append(current_context_tool)
tools.append(create_duckduckgo_search_tool)
 

# 2. Simple Calculation Tool (using Python's eval - be cautious with untrusted input)
def calculate(expression):
    """Evaluates a simple mathematical expression."""
    try:
        result = eval(expression)
        return f"The result of {expression} is: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"
 
calculation_tool = Tool(
    name="Calculator",
    func=calculate,
    description="useful for performing mathematical calculations. Input should be a valid Python expression.",
)
tools.append(calculation_tool)
 
# Initialize the AI agent
my_agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # Set to True to see the agent's internal reasoning
)
 




if __name__ == "__main__":
    duckduckgo_search = create_duckduckgo_search_tool()
 
    if duckduckgo_search:
        # Example usage of the tool directly (outside of an agent)
        query = "latest technology news"
        print(f"Searching DuckDuckGo for: '{query}'...")
        results = duckduckgo_search.run(query)
        print(f"Search Results:\n{results}")
 
        query_local_restaurants = "best vegetarian restaurants near me open now"
        print(f"\nSearching DuckDuckGo for: '{query_local_restaurants}'...")
        restaurant_results = duckduckgo_search.run(query_local_restaurants)
        print(f"Restaurant Results:\n{restaurant_results}")

    query1 = "What is the current time in our location?"
    print(f"User Query 1: {query1}")
    print(agent.run(query1))
 
    print("\n---")
 
    query2 = "Calculate 12 multiplied by 7."
    print(f"User Query 2: {query2}")
    print(agent.run(query2))
 
    print("\n---")
 
    query3 = "What is the current time plus 30 minutes?"
    print(f"User Query 3: {query3}")
    print(agent.run(query3))
 