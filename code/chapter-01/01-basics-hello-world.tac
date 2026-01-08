-- Hello World (agentic)
-- Smallest agentic Tactus procedure: send a message to an agent and return what it says.

world = Agent {
    provider = "openai",
    model = "gpt-4o-mini",
    system_prompt = "Your name is World."
}

output {
    message = field.string{required = true, description = "Agent response"}
}

local result = world({message = "Hello, World!"})

return {
    message = result.response
}
