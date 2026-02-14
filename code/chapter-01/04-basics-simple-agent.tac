-- Simple Agent Example

-- Mock configuration for testing (only active in mock mode)
Mocks {
    greeter = {
        tool_calls = {
            {tool = "done", args = {reason = "Hello! Welcome, it's wonderful to meet you!"}}
        },
        message = "Greeting produced"
    }
}

-- Define completion tool
-- snippet:start preface-simple-agent
local done = require("tactus.tools.done")

greeter = Agent {
    model = "openai/gpt-4o-mini",
    tool_choice = "required",
    system_prompt = [[You are a friendly assistant. When asked to greet someone, provide a warm, friendly greeting.

When you're done, call the done tool with reason set to your greeting message. Do not use emojis.]],
    initial_message = "Please greet the user with a friendly message",
    tools = {done},
}
-- snippet:end preface-simple-agent

Procedure {
    output = {
        greeting = field.string{required = true},
        completed = field.boolean{required = true},
    },
    function(input)
        -- snippet:start durable-checkpoint-loop
        local max_turns = 10
        local turn_count = 0

        done.reset()

        while not done.called() and turn_count < max_turns do
            turn_count = turn_count + 1
            greeter()
        end
        -- snippet:end durable-checkpoint-loop

        if done.called() then
            local call = done.last_call()
            local reason = (call and call.args and call.args.reason) or "Hello!"
            return {
                greeting = reason,
                completed = true
            }
        end

        return {
            greeting = "Agent did not complete properly",
            completed = false
        }
    end
}

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
