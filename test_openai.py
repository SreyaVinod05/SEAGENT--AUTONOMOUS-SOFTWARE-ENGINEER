from app.providers.openai_provider import OpenAIProvider

provider = OpenAIProvider()

response = provider.generate(
    "You are the first AI provider inside SEAGENT. "
    "Reply with a short welcome message."
)

print("\nSEAGENT OpenAI Response:")
print(response)