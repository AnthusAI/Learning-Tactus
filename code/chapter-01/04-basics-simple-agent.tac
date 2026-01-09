-- Simple Agent Example

-- Mock configuration for testing (only active in mock mode)
Mocks {
    greeter = {
        returns = {
            response = "Hello! Welcome, it's wonderful to meet you!",
            tool_calls = "done"
        }
    }
}

done = tactus.done

greeter = Agent {
    provider = "openai",
    model = "gpt-4o-mini",
    system_prompt = "You are a friendly assistant. When asked to greet someone, provide a warm, friendly greeting. When you're done, call the done tool with reason set to your greeting message. Do not use emojis.",
    initial_message = "Please greet the user with a friendly message",
    tools = {done},
}

output {
    greeting = field.string{required = true},
    completed = field.boolean{required = true},
}

local max_turns = 10
local turn_count = 0

while not done.called() and turn_count < max_turns do
    turn_count = turn_count + 1
    greeter()
end

if done.called() then
    local call = done.last_call()
    return {
        greeting = call.args.reason or "Hello!",
        completed = true
    }
else
    return {
        greeting = "Agent did not complete properly",
        completed = false
    }
end

-- BDD Specifications
Specifications([[
Feature: Simple Agent Interaction
  Demonstrate basic LLM agent interaction with done tool

  Scenario: Agent generates greeting using real LLM
    Given the procedure has started
    When the procedure runs
    Then the done tool should be called
    And the procedure should complete successfully
    And the output completed should be True
    And the output greeting should exist
    And the output greeting should not be "Agent did not complete properly"
    And the output greeting should match pattern "(Hello|Hi|Greetings|Welcome|hello|hi|greetings|welcome)"
]])
