# Agent Framework

This project is a modular framework for building intelligent agents that can execute complex tasks by orchestrating multiple components. The framework is designed to handle tasks such as querying databases, loading data, analyzing data, and generating reports.

## Project Structure

The project consists of the following key components:

### 1. `component_pool.py`
This file defines the `ComponentPool` class, which acts as a central repository for:
- **Methods**: Defines the available methods for each component type.
- **Plan Examples**: Provides example plans for each component type.
- **System Prompts**: Contains detailed prompts for guiding the agents in generating plans.

Key methods:
- `get_system_prompt(component_type)`: Returns the system prompt for a given component type.
- `get_plans(component_type)`: Returns example plans for a given component type.
- `get_methods(component_type)`: Returns the methods available for a given component type.

### 2. `agent_functions.py`
This file implements the `AgentFunctions` class, which contains the actual implementations of the methods defined in the `ComponentPool`. It also includes utility functions for interacting with an external LLM (Large Language Model) API.

Key methods:
- `generate_sql_query(inputs)`: Generates a SQL query based on a user prompt.
- `load_into_dataframe(inputs)`: Loads data from a database into a Pandas DataFrame.
- `generate_insights(inputs)`: Generates insights from a DataFrame.
- `create_chart(inputs)`: Creates a chart from a DataFrame.
- `generate_report(inputs)`: Generates a report combining insights and charts.

### 3. `agent_demo.py`
This file demonstrates the orchestration of agents to execute a user task. It defines the following classes:
- **Agent**: Represents an individual agent responsible for executing a specific component type.
- **Orchestrator**: A specialized agent that coordinates the execution of multiple components to fulfill a user task.
- **TaskQueue**: A queue for managing tasks.
- **Scheduler**: Responsible for assigning tasks to agents.
- **AgentPool**: Manages a pool of agents for different component types.

The `main()` function demonstrates the end-to-end execution of a task, starting from generating a plan to executing it and producing the final output.

### 4. External Dependencies
The project uses the following libraries:
- `pandas`: For data manipulation.
- `matplotlib`: For creating charts.
- `aiohttp`: For making asynchronous HTTP requests.
- `sqlite3`: For interacting with the SQLite database.

## How It Works

1. **Component Pool**: Defines the available methods, example plans, and system prompts for each component type.
2. **Agent Functions**: Implements the logic for each method.
3. **Agent Execution**: The `Agent` class generates a plan using the LLM and executes it step-by-step.
4. **Orchestration**: The `Orchestrator` coordinates multiple agents to complete a complex task.

## Running the Demo

To run the demo:
1. Ensure all dependencies are installed.
2. Execute the `agent_demo.py` file:
   ```bash
   python3 agent_demo.py
   ```
3. The orchestrator will generate a report based on the user prompt and display the final output.

## Example Output

For the user prompt: "Generate a report of revenue between the months of Jan and Dec", the framework will:
1. Generate a SQL query to fetch the data.
2. Load the data into a DataFrame.
3. Analyze the data to generate insights and charts.
4. Combine the insights and charts into a report.

The final output will include the generated report and the path to the saved chart.

## Future Enhancements

- Add support for more complex workflows.
- Improve error handling and retries for LLM interactions.
- Extend the framework to support additional data sources and visualization types.

## License

This project is licensed under the MIT License.
