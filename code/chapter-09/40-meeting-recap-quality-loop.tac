-- Meeting Recap Quality Loop
-- Demonstrates a safe agent loop with deterministic checks and bounded retries.

-- snippet:start per-turn-tool-control
-- worker({tools = {}})              -- no tools this turn
-- worker({tools = {search, done}})  -- only these tools
-- snippet:end per-turn-tool-control

finalize_recap = Tool {
    description = "Capture recap email fields as structured data",
    input = {
        subject = field.string{required = true},
        body = field.string{required = true},
        action_items = field.array{required = true}
    },
    function(args)
        return {status = "captured"}
    end
}

recapper = Agent {
    model = {
        name = "openai/gpt-4o-mini",
        temperature = 0.2
    },
    tool_choice = "required",
    system_prompt = [[You turn messy meeting notes into a clean recap email.

You have one tool:
- finalize_recap: call this exactly once with (subject, body, action_items)

Rules:
- Do NOT invent facts. If something is missing, write "TBD".
- body must be plain text (not Markdown).
- action_items must be an array of short strings.
- If given "Issues to fix", address them explicitly in the next draft.
- After calling finalize_recap, stop. Do not output anything else.]],
    tools = {finalize_recap}
}

local function contains_action_language(text)
    local lower = string.lower(text or "")
    return string.find(lower, "action") ~= nil or string.find(lower, "todo") ~= nil
end

local function has_any_action_item(action_items)
    if action_items == nil then
        return false
    end

    -- In mock mode and some runtimes, arrays may arrive as Python lists (0-indexed).
    local ok0, first0 = pcall(function()
        return action_items[0]
    end)
    if ok0 and first0 ~= nil then
        return true
    end

    -- In Lua tables, arrays are typically 1-indexed.
    local ok1, first1 = pcall(function()
        return action_items[1]
    end)
    return ok1 and first1 ~= nil
end

local function validate_draft(draft, raw_notes)
    local issues = {}

    if not draft.subject or draft.subject == "" then
        table.insert(issues, "Subject is empty")
    elseif #draft.subject > 80 then
        table.insert(issues, "Subject must be <= 80 characters")
    end

    if not draft.body or #draft.body < 80 then
        table.insert(issues, "Body is too short to be useful")
    end

    if contains_action_language(raw_notes) then
        if not has_any_action_item(draft.action_items) then
            table.insert(issues, "Expected at least one action item")
        end
    end

    return #issues == 0, issues
end

Procedure {
    input = {
        recipient_name = field.string{default = "Sam"},
        raw_notes = field.string{
            default = "Discussed Q1 launch timeline. Risks: vendor delays. Action: Sam to confirm dates by Friday."
        }
    },
    output = {
        subject = field.string{required = true},
        body = field.string{required = true},
        action_items = field.array{required = true},
        attempts = field.number{required = true}
    },
    function(input)
        local base_message = "Recipient: " .. input.recipient_name .. "\n\nNotes:\n" .. input.raw_notes

        -- snippet:start safe-loop-shape
        local max_attempts = 3
        local attempt = 0

        local ok = false
        local issues = {}
        local draft = {}

        while attempt < max_attempts do
            attempt = attempt + 1
            Log.info("Draft attempt", {attempt = attempt})

            local message = base_message
            if #issues > 0 then
                message = message .. "\n\nIssues to fix:\n- " .. table.concat(issues, "\n- ")
            end

            local max_turns = 3
            local turn_count = 0

            finalize_recap.reset()

            while not finalize_recap.called() and turn_count < max_turns do
                turn_count = turn_count + 1
                recapper({message = message})
            end

            assert(finalize_recap.called(), "Agent did not call finalize_recap")

            local call = finalize_recap.last_call()
            draft = (call and call.args) or {}

            ok, issues = validate_draft(draft, input.raw_notes)
            if ok then
                break
            end

            Log.warn("Draft failed checks", {issues = issues})
        end

        assert(ok, "Failed to produce an acceptable draft after " .. max_attempts .. " attempts")
        -- snippet:end safe-loop-shape

        return {
            subject = draft.subject or "TBD",
            body = draft.body or "TBD",
            action_items = draft.action_items or {},
            attempts = attempt
        }
    end
}

Mocks {
    recapper = {
        tool_calls = {
            {
                tool = "finalize_recap",
                args = {
                    subject = "Q1 launch timeline recap",
                    body = "Hi Sam,\n\nQuick recap from today:\n- Reviewed Q1 launch timeline\n- Flagged risk: vendor delays\n\nAction items:\n- Sam: confirm dates by Friday\n\nThanks,",
                    action_items = {"Sam: confirm dates by Friday"}
                }
            }
        },
        message = "Drafted recap email"
    }
}

Specifications([[
Feature: Meeting recap quality loop
  Iterate safely until the draft passes deterministic checks

  Scenario: Draft passes checks without retries (mock mode)
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the finalize_recap tool should be called
    And the output attempts should be 1
]])
