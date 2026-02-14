-- Meeting Recap with Human-in-the-Loop and Send Tool (Stubbed)
-- Demonstrates Human.review + Human.approve gates before calling a tool.

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
        to = field.string{required = true},
        subject = field.string{required = true},
        body = field.string{required = true}
    },
    function(args)
        Log.info("Stub send_email called", {to = args.to, subject = args.subject})
        return {message_id = "msg_stub_001"}
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
- After calling finalize_recap, stop. Do not output anything else.]],
    tools = {finalize_recap}
}

local function draft_from_notes(recipient_name, raw_notes, extra_instructions)
    local message = "Recipient: " .. recipient_name .. "\n\nNotes:\n" .. raw_notes
    if extra_instructions and extra_instructions ~= "" then
        message = message .. "\n\nInstructions:\n" .. extra_instructions
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
    return (call and call.args) or {}
end

Procedure {
    input = {
        recipient_name = field.string{default = "Sam"},
        recipient_email = field.string{default = "sam@example.com"},
        raw_notes = field.string{
            default = "Discussed Q1 launch timeline. Risks: vendor delays. Action: Sam to confirm dates by Friday."
        }
    },
    output = {
        subject = field.string{required = true},
        body = field.string{required = true},
        action_items = field.array{required = true},
        approved = field.boolean{required = true},
        sent = field.boolean{required = true},
        message_id = field.string{description = "Fake id returned by send_email"}
    },
    function(input)
        Log.info("Drafting recap email")

        local draft = draft_from_notes(input.recipient_name, input.raw_notes, "")

        local artifact = {
            to = input.recipient_email,
            subject = draft.subject or "TBD",
            body = draft.body or "TBD",
            action_items = draft.action_items or {}
        }

        local review = Human.review({
            message = "Review recap email draft",
            artifact = artifact,
            artifact_type = "document",
            options = {
                {label = "Approve", type = "action"},
                {label = "Revise", type = "action"},
                {label = "Reject", type = "cancel"}
            }
        })

        local decision = review and review.decision or "Reject"
        if decision == "Reject" then
            error("Draft rejected by reviewer")
        end

        if decision == "Revise" then
            if review.edited_artifact then
                artifact = review.edited_artifact
            elseif review.feedback and review.feedback ~= "" then
                local revised = draft_from_notes(
                    input.recipient_name,
                    input.raw_notes,
                    "Revise the draft using this feedback: " .. review.feedback
                )
                artifact.subject = revised.subject or artifact.subject
                artifact.body = revised.body or artifact.body
                artifact.action_items = revised.action_items or artifact.action_items
            end
        end

        local approved = Human.approve({
            message = "Send this email now?",
            context = {to = artifact.to, subject = artifact.subject},
            timeout = 3600,
            default = false
        })

        if not approved then
            Log.warn("Not approved to send")
            return {
                subject = artifact.subject,
                body = artifact.body,
                action_items = artifact.action_items,
                approved = false,
                sent = false
            }
        end

        local send_result = send_email({
            to = artifact.to,
            subject = artifact.subject,
            body = artifact.body
        })

        return {
            subject = artifact.subject,
            body = artifact.body,
            action_items = artifact.action_items,
            approved = true,
            sent = true,
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
Feature: Meeting recap with HITL gates
  Review and approve before calling the send tool

  Scenario: Review approves and send is approved (mock mode)
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the finalize_recap tool should be called
    And the send_email tool should be called
    And the output sent should be True
]])
