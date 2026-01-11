-- Loop Shapes (for docs)
-- Contains small code excerpts used in the Agent Loop chapter.

-- snippet:start safe-loop-shape
-- local max_attempts = 3
-- local attempt = 0
--
-- while attempt < max_attempts do
--   attempt = attempt + 1
--
--   -- take a turn (agent call, tool call, etc.)
--
--   if success then
--     break
--   end
-- end
--
-- assert(success, "Failed to produce an acceptable result after " .. max_attempts .. " attempts")
-- snippet:end safe-loop-shape

Procedure {
    output = {
        ok = field.boolean{required = true}
    },
    function(input)
        return {ok = true}
    end
}

Specifications([[
Feature: Loop shapes
  Scenario: File is valid
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
]])
