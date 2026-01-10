-- Meeting Recap Draft (Part II running example)
-- First version: return a single draft string.

Mocks {
    recapper = {
        tool_calls = {},
        message = [[Subject: Q1 launch timeline recap

Hi Sam,

Quick recap from today:
- Reviewed Q1 launch timeline
- Flagged risk: vendor delays

Action items:
- Sam: confirm dates by Friday

Thanks,]]
    }
}

recapper = Agent {
    provider = "openai",
    model = {
        name = "gpt-4o-mini",
        temperature = 0.2
    },
    system_prompt = [[You turn messy meeting notes into a clean recap email.

Rules:
- Do NOT invent facts. If something is missing, write "TBD".
- Output plain text (not Markdown).
- Format exactly:
  Subject: <one line>

  Hi <recipient_name>,

  <short recap paragraph or bullets>

  Action items:
  - <bullets, if any>

  Thanks,]],
}

Procedure {
    input = {
        recipient_name = field.string{
            default = "Sam",
            description = "Who the email is addressed to"
        },
        raw_notes = field.string{
            default = "Discussed Q1 launch timeline. Risks: vendor delays. Action: Sam to confirm dates by Friday.",
            description = "Messy meeting notes, transcript, or pasted bullets"
        }
    },
    output = {
        draft = field.string{required = true, description = "Draft email (subject + body)"}
    },
    function(input)
        local message = "Recipient: " .. input.recipient_name .. "\n\nNotes:\n" .. input.raw_notes
        local result = recapper({message = message})

        if result and result.message and result.message ~= "" then
            return {draft = result.message}
        end

        return {draft = "No draft produced"}
    end
}

Specifications([[
Feature: Meeting recap draft (unstructured)
  Generate a recap email draft from raw notes

  Scenario: Produces a draft string
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
    And the output draft should exist
]])
