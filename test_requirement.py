from app.agents.Requirement import RequirementAnalysisAgent


agent = RequirementAnalysisAgent()

requirement = """
Create an online food ordering website.
Users should be able to browse restaurants,
view menus and place orders.
"""

result = agent.analyze(requirement)

print(result)