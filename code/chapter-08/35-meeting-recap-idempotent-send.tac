-- Meeting Recap with Idempotent Send (Stubbed)
-- Demonstrates using state + stages to make side effects retry-safe.

Stages({"drafting", "sending", "complete"})

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

send_email = Tool {
    description = "Send an email (stubbed in this repo; returns a fake message_id)",
    input = {
        to = field.string{required = true, description = "Recipient email address"},
        subject = field.string{required = true, description = "Email subject"},
        body = field.string{required = true, description = "Email body"},
        idempotency_key = field.string{description = "Stable key to de-duplicate sends (if your provider supports it)"}
    },
    function(args)
        Log.info("Stub send_email called", {to = args.to, subject = args.subject, idempotency_key = args.idempotency_key})
        return {message_id = "msg_stub_001"}
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
        message_id = field.string{required = true},
        send_attempts = field.number{required = true}
    },
    state = {
        message_id = field.string{description = "External message id (guards against double send)"},
        send_attempts = field.number{description = "Count of actual send attempts", default = 0},
        idempotency_key = field.string{description = "Stable key to de-duplicate sends"},
        draft_subject = field.string{description = "Draft subject (for debugging)"},
        draft_body = field.string{description = "Draft body (for debugging)"},
        draft_action_items = field.array{description = "Draft action items (for debugging)"}
    },
    function(input)
        Stage.set("drafting")

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

        state.draft_subject = draft.subject or "TBD"
        state.draft_body = draft.body or "TBD"
        state.draft_action_items = draft.action_items or {}

        local function send_once()
            if state.message_id then
                Log.info("Skipping send (already sent)", {message_id = state.message_id})
                return state.message_id
            end

            Stage.set("sending")

            State.increment("send_attempts")
            state.idempotency_key = state.idempotency_key or ("recap:" .. input.recipient_email .. ":" .. (input.raw_notes or ""))

            local result = send_email({
                to = input.recipient_email,
                subject = state.draft_subject,
                body = state.draft_body,
                idempotency_key = state.idempotency_key
            })

            state.message_id = result.message_id
            return state.message_id
        end

        local first_id = send_once()

        -- Simulate a retry or re-entry into the "send" step.
        local second_id = send_once()
        assert(second_id == first_id, "Idempotency guard failed: message id changed")

        Stage.set("complete")

        return {
            subject = state.draft_subject,
            body = state.draft_body,
            action_items = state.draft_action_items or {},
            message_id = state.message_id,
            send_attempts = state.send_attempts or 0
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
Feature: Idempotent send step
  Use state to guard side effects so retries don't double-send

  Scenario: Send is only performed once
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the send_email tool should be called exactly 1 time
    And the state message_id should exist
    And the state send_attempts should be 1
    And the stage should be complete
]])
