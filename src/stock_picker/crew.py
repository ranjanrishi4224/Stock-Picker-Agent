from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool


@CrewBase
class StockPicker:
    """Stock Picker Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_finder"],
            tools=[SerperDevTool()],
            verbose=True,
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],
            tools=[SerperDevTool()],
            verbose=True,
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],
            verbose=True,
        )

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies"],
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_companies"],
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config["pick_best_company"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Stock Picker Crew"""

        manager = Agent(
            config=self.agents_config["manager"],
            allow_delegation=True,
            verbose=True,
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            manager_agent=manager,
            process=Process.hierarchical,
            verbose=True,
        )