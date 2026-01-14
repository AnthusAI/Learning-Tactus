-- Test streaming with a simple LLM agent

poet = Agent {
    provider = "openai",
    model = "gpt-4o-mini",
    temperature = 0.7,
    stream = true,
    system_prompt = "You are a haiku poet. Write beautiful haikus."
}

Procedure {
    output = {
        poem = field.string{required = true}
    },
    function(input)
        poet({message = "Write a haiku about streaming data in real-time"})

        return {
            poem = "Streaming test completed successfully"
        }
    end
}
