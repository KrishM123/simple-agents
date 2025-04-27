import pandas as pd
import matplotlib.pyplot as plt
import os
import aiohttp
import sqlite3


async def send_llm_request(system_prompt, query):
    url = "http://10.123.99.101:15001/generate"
    headers = {"Content-Type": "application/json"}

    payload = {
        "project_id": "5d439c42-11d1-49b1-8cab-a24f7f730d61",
        "backend": "vllm",
        "is_cluster_mode": True,
        "model_name": "llama3:8b",
        "user_id": "user_1",
        "session_id": "240d5f92-9629-40f7-a2a0-b719cb163152",
        "prompt": system_prompt + query,
        "prompt_token_ids": [],
        "query": "",
        "query_token_ids": [],
        "stream": False,
        "doc_ids": [11],
        "is_kv_ready": [True],
        "rai": True,
        "long_mem_window": 5,
        "short_mem_window": 10,
        "temperature": 0.0,
        "ignore_eos": False,
        "presence_penalty": 2,
        "max_tokens": 1000
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Request failed with status code {response.status}")
                response_data = await response.json()
                return response_data.get("output")
    except Exception as e:
        print(f"[LLM Gateway] Error: {str(e)}")
        return ""


async def format_llm_response(format, example, error, incorrect_output):
    print(f"Failed to parse {incorrect_output}. Trying again.")
    return await send_llm_request("You've generated an incorrect response. I will include info about the incorrect response annd I want you to fix it and return it.", f"The following response was not correct: {incorrect_output} with this error: {error}. I want you to format it in this format: {format}. Here is a correct example: {example}")


class AgentFunctions:
    def __init__(self):
        self.methods = {
            'generate_sql_query': self.generate_sql_query,
            'load_into_dataframe': self.load_into_dataframe,
            'generate_insights': self.generate_insights,
            'create_chart': self.create_chart,
            'generate_report': self.generate_report
        }
    

    async def get_method(self, method_name):
        method = self.methods.get(method_name)
        if not method:
            raise ValueError(f"Method {method_name} not found.")
        return method


    async def generate_sql_query(self, inputs):
        query_plan = await send_llm_request("There is a sqlite database with monthly_revenue table with revenue and month columns. Make a SQL Query from this prompt: ", inputs['prompt'])
        query_plan = "SELECT * FROM monthly_revenue"
        return {"sql_query": query_plan}


    async def load_into_dataframe(self, inputs):
        conn = sqlite3.connect('./database/revenue.db')
        df = pd.read_sql_query(inputs['sql_query'], conn)
        conn.close()
        return {"dataframe": df}


    async def generate_insights(self, inputs):
        insights = await send_llm_request("Generate insights for this dataframe: ", str(inputs['dataframe'].describe().to_dict()) + inputs['prompt'])
        return {"insights": insights}


    async def create_chart(self, inputs, chart_type="bar", x_col=None, y_col=None, output_dir="charts"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.figure(figsize=(10, 6))
        plt.bar(inputs['dataframe']["month"], inputs['dataframe']["revenue"], color='skyblue')

        plt.xticks(rotation=45)

        file_path = os.path.join(output_dir, chart_type + "_chart.png")
        plt.tight_layout()
        plt.savefig(file_path)

        return {"chart": file_path}


    async def generate_report(self, inputs, output_dir="reports"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        report_path = os.path.join(output_dir, "data_report.txt")
        with open(report_path, "w") as f:
            f.write("Data Report\n")
            f.write("="*50 + "\n\n")

            f.write(f"Insights: {inputs['insights']}\n\n")
            f.write(f"Chart saved at: {inputs['chart']}\n")

        return {'report': report_path}