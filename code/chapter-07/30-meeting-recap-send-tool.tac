-- Meeting Recap + Send Tool (Stubbed)
-- Demonstrates defining and calling tools, and using a "finalize" tool to capture structured output.

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

-- snippet:start send-email-tool
send_email = Tool {
    description = "Send an email (stubbed in this repo; returns a fake message_id)",
    input = {
        to = field.string{required = true, description = "Recipient email address"},
        subject = field.string{required = true, description = "Email subject"},
        body = field.string{required = true, description = "Email body"}
    },
    function(args)
        Log.info("Stub send_email called", {to = args.to, subject = args.subject})
        return {message_id = "msg_12345"}
    end
}
-- snippet:end send-email-tool

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
        recipient_email = field.string{default = "sam@example.com", description = "Where to send the email"},
        raw_notes = field.string{
            default = "Discussed Q1 launch timeline. Risks: vendor delays. Action: Sam to confirm dates by Friday.",
            description = "Messy meeting notes, transcript, or pasted bullets"
        }
    },
    output = {
        subject = field.string{required = true},
        body = field.string{required = true},
        action_items = field.array{required = true},
        message_id = field.string{required = true, description = "Fake id returned by send_email"}
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
        local draft = (call and call.args) or {}

        local send_result = send_email({
            to = input.recipient_email,
            subject = draft.subject or "TBD",
            body = draft.body or "TBD"
        })

        return {
            subject = draft.subject or "TBD",
            body = draft.body or "TBD",
            action_items = draft.action_items or {},
            message_id = send_result.message_id
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
Feature: Meeting recap with send tool (stubbed)
  Draft a recap email and call a stubbed send tool

  Scenario: Sends the drafted email
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the finalize_recap tool should be called
    And the send_email tool should be called
    And the output message_id should exist
]])
