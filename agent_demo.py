import asyncio
from agent_functions import *
from component_pool import ComponentPool
from agent_functions import *
import json


class Agent:
    def __init__(self, component_pool, component_type):
        self.component_pool = component_pool
        self.component_type = component_type
        self.methods = component_pool.get_methods(component_type)
        self.system_prompt = component_pool.get_system_prompt(component_type)
        self.data_store = {}
        self.functions = AgentFunctions()

    async def execute(self, inputs):
        print(f"\n[{self.component_type}] Executing pipeline for query: {inputs['prompt']}")
        if inputs:
            print(f"[{self.component_type}] Inputs: {inputs}")
            for key, value in inputs.items():
                self.data_store[key] = value

        plan = await self._generate_plan(inputs['prompt'])
        print(f"[{self.component_type}] Plan generated with {len(plan)} steps")

        results = await self._execute_plan(plan)
        return results

    async def _generate_plan(self, query):
        query = f"Generate detailed action plan for: {query} \n\n"
        plan_text = await self._query_llm_for_plan(query)
        return await self._parse_plan_text(plan_text)

    async def _query_llm_for_plan(self, query):
        await send_llm_request(f"System Prompt: {self.system_prompt}", f". Query {query}")
        return component_pool.get_plans(self.component_type)

    async def _parse_plan_text(self, plan_text):
        max_attempts = 3
        attempt = 0
        steps = []
        while attempt < max_attempts:
            try:
                steps = json.loads(plan_text)
                break
            except json.JSONDecodeError as e:
                attempt += 1
                plan_text = await format_llm_response(
                    component_pool.plan_format,
                    component_pool.get_plans(self.component_type),
                    f"Error parsing JSON on attempt {attempt}: {e}",
                    plan_text
                )
                if attempt >= max_attempts:
                    return []
        
        return steps

    async def _execute_plan(self, plan):
        for step in plan:
            method_name = step["method"]
            method = await self.functions.get_method(method_name)

            if method:
                inputs = self._collect_inputs(step)
                output_data = await method(inputs)
                if output_data is not None:
                    self._store_outputs(output_data)
    
            else:
                print(f"[{self.component_type}] ⚠️ Method {method_name} not found!")
        return self.data_store
    
    def _collect_inputs(self, step):
        required_inputs = component_pool.get_methods(self.component_type)[step["method"]]["inputs"]
        inputs = {}
        for inp in required_inputs:
            if inp in self.data_store:
                inputs[inp] = self.data_store[inp]
            else:
                inputs["info"] = inp
        return inputs

    def _store_outputs(self, output_data):
        for key, value in output_data.items():
            self.data_store[key] = value


class Orchestrator(Agent):
    def __init__(self, task_queue, component_pool, scheduler, agent_pool):
        self.task_queue = task_queue
        self.component_pool = component_pool
        self.functions = scheduler
        self.agent_pool = agent_pool
        self.component_type = "orchestrator"
        self.methods = component_pool.get_methods(self.component_type)
        self.system_prompt = component_pool.get_system_prompt(self.component_type)
        self.data_store = {}


class TaskQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, task):
        task_id = id(task)
        await self.queue.put(task)
        return task_id


class Scheduler:
    def __init__(self, agent_pool):
        self.agent_pool = agent_pool

    async def get_method(self, component):
        return await self.agent_pool.get_agent(component)


class AgentPool:
    def __init__(self, component_pool):
        self.component_pool = component_pool
        self.agents = {}

    async def get_agent(self, component):
        if component not in self.agents:
            self.agents[component] = Agent(self.component_pool, component)
        return self.agents[component].execute


component_pool = ComponentPool()
task_queue = TaskQueue()
agent_pool = AgentPool(component_pool)
scheduler = Scheduler(agent_pool)
orchestrator = Orchestrator(task_queue, component_pool, scheduler, agent_pool)


async def main():
    user_prompt = "Generate a report of revenue between the months of Jan and Dec"
    result = await orchestrator.execute({'prompt': user_prompt})
    print("\n=== FINAL OUTPUT ===")
    print(result)

asyncio.run(main())