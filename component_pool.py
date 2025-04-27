class ComponentPool:
    def __init__(self):
        self.plan_format = """
                            [
                                {
                                    "method": "<method_name_1>"
                                },
                                {
                                    "method": "<method_name_2>"
                                }
                                ...
                            ]
                            """
        self.methods = {
            "query_database": {"generate_sql_query": {
                "inputs": ["prompt"],
                "outputs": ["sql_query"]}
            },
            "load_data": {
                "load_into_dataframe": {
                    "inputs": ["sql_query"],
                    "outputs": ["dataframe"]
                }
            },
            "analyze_data": {
                "create_chart": {
                    "inputs": ["dataframe"],
                    "outputs": ["chart"]
                },
                "generate_insights": {
                    "inputs": ["dataframe", "prompt"],
                    "outputs": ["insights"]
                }
            },
            "generate_report": {
                "generate_report": {
                    "inputs": ["insights", "chart", "prompt"],
                    "outputs": ["report"]
                }
            },
            "orchestrator": {
                "query_database": {
                    "inputs": ["prompt"],
                    "outputs": ["sql_query"]
                },
                "load_data": {
                    "inputs": ["prompt", "sql_query"],
                    "outputs": ["dataframe"]
                },
                "analyze_data": {
                    "inputs": ["prompt", "dataframe", "prompt"],
                    "outputs": ["chart", "insights"]
                },
                "generate_report": {
                    "inputs": ["prompt", "insights", "chart", "prompt"],
                    "outputs": ["report"]
                }
            }
        }
        self.plan_examples = {
            "query_database": """[
                                    {
                                        "method": "generate_sql_query"
                                    }
                                ]""",
            "load_data": """[
                                {
                                    "method": "load_into_dataframe"
                                }
                            ]""",
            "analyze_data": """[
                                    {
                                        "method": "create_chart"
                                    },
                                    {
                                        "method": "generate_insights"
                                    }
                                ]""",
            "generate_report": """[
                                        {
                                            "method": "generate_report"
                                        }
                                    ]""",
            "orchestrator": """[
                                    {
                                        "method": "query_database"
                                    },
                                    {
                                        "method": "load_data"
                                    },
                                    {
                                        "method": "analyze_data"
                                    },
                                    {
                                        "method": "generate_report"
                                    }
                                ]""",
        }
        self.system_prompts = {
            "query_database": f"""You are an intelligent agent tasked with generating a plan to query the database. 
                                The database has a table called monthly_revenue that contains month and revenue columns.
                                I want you to create a plan to generate a sql query that gets the necessary information from the database.
                                The plan should be in this format: {self.plan_format}.
                                Here are the methods you have at your disposal: {self.methods["query_database"]}
                                Here is an example plan for the prompt: "Generate a report of revenue between the months of Oct and Dec"
                                {self.plan_examples["query_database"]}.
                                Make sure the plan is accurate and in the correct format.
                                Carefully understand the input and outputs of methods to use.
                                """,
            "load_data": f"""System Prompt: You are a data loader assistant. Your task is to execute SQL queries and load the resulting data into a dataframe. 
                            There are methods to help you execute SQL queries and load into dataframe, you just have to come up with the right plan.
                            The plan should be in this format: {self.plan_format}.
                            Here are the methods you have at your disposal: {self.methods["load_data"]}
                            Here is an example plan for the prompt: "Generate a report of revenue between the months of Oct and Dec"
                            {self.plan_examples["load_data"]}.
                            Make sure the plan is accurate and in the correct format.
                            Carefully understand the input and outputs of methods to use.
                            """,
            "analyze_data": f"""System Prompt: You are a data analysis assistant. Your task is to analyze the given dataframe by either generating visualizations or deriving insights from the data. 
                                There are methods to help generate insights and charts, but you have to tell generate instights exactly what to do through the plan you develop.
                                The plan should be in this format: {self.plan_format}.
                                Here are the methods you have at your disposal: {self.methods["analyze_data"]}
                                Here is an example plan for the prompt: "Generate a report of revenue between the months of Oct and Dec"
                                {self.plan_examples["analyze_data"]}.
                                Make sure the plan is accurate and in the correct format.
                                Carefully understand the input and outputs of methods to use.
                                """,
            "generate_report": f"""System Prompt: You are a report generation assistant. Your task is to create a comprehensive report by combining insights, charts, and a prompt. 
                                The plan should be in this format: {self.plan_format}.
                                Here are the methods you have at your disposal: {self.methods["generate_report"]}
                                Here is an example plan for the prompt: "Generate a report of revenue between the months of Oct and Dec"
                                {self.plan_examples["generate_report"]}.
                                Make sure the plan is accurate and in the correct format.
                                Carefully understand the input and outputs of methods to use.
                                """,
            "orchestrator": f"""You are an orchestrator agent tasked with generating a detailed, structured action plan for completing a user task. 

                                Your output should follow this specific format and return nothing else. Only the json, no extra output, no extra notes, NOTHING EXTRA:
                                {self.plan_format}

                                The agents you have at your disposal are:
                                {self.methods["orchestrator"]}

                                Here is an example plan for the prompt: "Generate a report of revenue between the months of Oct and Dec"
                                {self.plan_examples["orchestrator"]}.

                                Please ensure that:
                                - Return no extra explaination text
                                - The plan should be ordered logically and sequentially.
                                - The methods should be agents or functions that your system can invoke.
                                - Only choose a method if it's inputs have been outputted by another method previously

                                Your job is to return the correct structured plan for each user request.
                        """
        }

    def get_system_prompt(self, component_type):
        return self.system_prompts[component_type]
    
    def get_plans(self, component_type):
        return self.plan_examples[component_type]
    
    def get_methods(self, component_type):
        return self.methods[component_type]