-- Meeting Recap Draft (Structured Output)
-- Demonstrates procedure inputs/outputs + a "finalize" tool for structured results.

finalize_recap = Tool {
    description = "Capture recap email fields as structured data",
    input = {
        subject = field.string{required = true, description = "Email subject line"},
        body = field.string{required = true, description = "Email body (plain text)"},
        action_items = field.array{required = true, description = "Action items (strings)"}
    },
    function(args)
        return {status = "captured"}
    end
}

recapper = Agent {
    provider = "openai",
    model = {
        name = "gpt-4o-mini",
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
- After calling finalize_recap, stop. Do not output anything else.]],
    tools = {finalize_recap}
}

Procedure {
    input = {
        recipient_name = field.string{default = "Sam", description = "Who the email is addressed to"},
        raw_notes = field.string{
            default = "Discussed Q1 launch timeline. Risks: vendor delays. Action: Sam to confirm dates by Friday.",
            description = "Messy meeting notes, transcript, or pasted bullets"
        }
    },
    output = {
        subject = field.string{required = true, description = "Draft subject"},
        body = field.string{required = true, description = "Draft body"},
        action_items = field.array{required = true, description = "Draft action items"}
    },
    function(input)
        local message = "Recipient: " .. input.recipient_name .. "\n\nNotes:\n" .. input.raw_notes

        local max_turns = 3
        local turn_count = 0

        finalize_recap.reset()

        while not finalize_recap.called() and turn_count < max_turns do
            turn_count = turn_count + 1
            recapper({message = message})
        end

        assert(finalize_recap.called(), "Agent did not call finalize_recap")
        local call = finalize_recap.last_call()
        local args = (call and call.args) or {}

        return {
            subject = args.subject or "TBD",
            body = args.body or "TBD",
            action_items = args.action_items or {}
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
Feature: Meeting recap with structured output
  Produce a structured recap draft (subject/body/action_items)

  Scenario: Returns structured fields
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the finalize_recap tool should be called
    And the output subject should exist
    And the output body should exist
    And the output action_items should exist
]])

