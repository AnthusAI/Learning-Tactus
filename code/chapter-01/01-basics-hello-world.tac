-- Hello World (Smallest agentic Tactus program)
--
-- This file is intentionally tiny. For consistency with the rest of the book
-- (and to keep it testable in CI), we wrap the call in a Procedure and include
-- a simple mock configuration and BDD spec.

Mocks {
    World = {
        tool_calls = {},
        message = "Hello! It's great to meet you. How can I assist you today?"
    }
}

-- snippet:start hello-world-program
World = Agent {
    provider = "openai",
    model = "gpt-4o-mini",
    system_prompt = "Your name is World."
}

Procedure {
    output = {
        message = field.string{required = true}
    },
    function(input)
        local result = World({message = "Hello, World!"})
        local message = (result and (result.message or result.response)) or ""
        return {message = message}
    end
}
-- snippet:end hello-world-program

Specifications([[
Feature: Hello world
  Scenario: Agent returns a greeting
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the output message should exist
    And the output message should match pattern "(Hello|Hi|Greetings|Welcome|hello|hi|greetings|welcome)"
]])
