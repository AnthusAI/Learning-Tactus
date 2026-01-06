-- code/chapter-03/contact-processor.tac
-- A complete agent for processing contact data
-- Demonstrates everything-as-code: tools, agent, orchestration, and tests in one file

-- Tools give the agent capabilities
Tool "file_contact" {
    description = "Save a processed contact to the database",
    input = {
        name = field.string{required = true},
        email = field.string{required = true},
        company = field.string{required = false}
    },
    function(args)
        -- In a real system, this would save to a database
        Log.info("Filed contact", args)
        return "Contact filed: " .. args.name
    end
}

Tool "done" {
    description = "Signal that all contacts have been processed",
    input = {
        count = field.number{required = true, description = "Number of contacts processed"}
    },
    function(args)
        return "Processed " .. args.count .. " contacts"
    end
}

-- Agent configuration
Agent "processor" {
    provider = "openai",
    model = "gpt-4o-mini",
    system_prompt = [[You are a contact data processor.

Given raw contact data in any format (CSV lines, JSON, plain text),
extract each contact and call file_contact for each one.

When all contacts are processed, call done with the count.

Handle messy data gracefully:
- Infer fields when possible
- Skip entries with insufficient data
- Be forgiving of formatting variations]],
    toolsets = {"file_contact", "done"}
}

-- Orchestration logic
Procedure "main" {
    input = {
        data = field.string{required = true, description = "Raw contact data to process"}
    },
    output = {
        processed_count = field.number{required = true},
        status = field.string{required = true}
    },
    function(input)
        -- Give agent the data
        Agent("processor").turn({
            inject = "Process these contacts:\n\n" .. input.data
        })

        -- Let it work until done
        local max_turns = 20
        local turn_count = 0

        repeat
            Agent("processor").turn()
            turn_count = turn_count + 1
        until Tool.called("done") or turn_count >= max_turns

        -- Collect results
        if Tool.called("done") then
            local count = Tool.last_call("done").args.count
            return {
                processed_count = count,
                status = "Completed successfully"
            }
        else
            return {
                processed_count = 0,
                status = "Max turns reached without completion"
            }
        end
    end
}

-- Behavior specifications
Specifications([[
Feature: Contact Processing

  Scenario: Processes multiple contacts
    Given the procedure has started
    When the processor agent takes turns
    Then the file_contact tool should be called at least once
    And the done tool should be called exactly once
    And the procedure should complete successfully

  Scenario: Handles completion
    Given the procedure has started
    When the processor agent takes turns
    Then the output processed_count should be greater than 0
    And the output status should be "Completed successfully"
]])
