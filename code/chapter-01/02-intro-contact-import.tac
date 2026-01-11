-- Intro Example: Import One Contact (Give an Agent a Tool)
--
-- This is a runnable counterpart to the introduction’s code snippet.
-- It defines a local `file_contact` tool (as a stub) so the agent has a real capability to call.

-- snippet:start intro-snippet
-- input {
--     raw_contact = field.string{required = true, description = "One contact record as raw text"}
-- }
--
-- importer = Agent {
--     provider = "openai",
--     model = "gpt-4o-mini",
--     system_prompt = [[
-- You will be given one contact record as raw text.
-- It might be a 1-row CSV (with header), a JSON object, or an email header.
-- Extract first name, last name, email, and notes (if present), then call file_contact exactly once.
--     ]],
--     tools = {file_contact},
-- }
--
-- output {
--     contact_id = field.string{required = true},
-- }
--
-- importer({message = "Import this contact record:\n" .. input.raw_contact})
--
-- assert(file_contact.called(), "Agent did not call file_contact")
--
-- return {
--     contact_id = file_contact.last_result()
-- }
-- snippet:end intro-snippet

-- Mock configuration for testing (only active in mock mode)
Mocks {
    importer = {
        tool_calls = {
            {
                tool = "file_contact",
                args = {
                    first_name = "FIRST",
                    last_name = "LAST",
                    email = "contact@example.com",
                    notes = "VIP",
                }
            }
        },
        message = "Filed contact"
    }
}

file_contact = Tool {
    description = "Create a contact in our CRM (stub for the book example)",
    input = {
        first_name = field.string{required = true},
        last_name = field.string{required = true},
        email = field.string{required = true},
        notes = field.string{default = ""},
    },
    function(args)
        -- In a real app, this would call your CRM API and return an ID.
        return "contact_" .. args.email
    end
}

importer = Agent {
    provider = "openai",
    model = "gpt-4o-mini",
    system_prompt = [[
You will be given one contact record as raw text.
It might be a 1-row CSV (with header), a JSON object, or an email header.
Extract first name, last name, email, and notes (if present), then call file_contact exactly once.
    ]],
    tools = {file_contact},
}

Procedure {
    input = {
        raw_contact = field.string{
            description = "One contact record as raw text (CSV header+row, JSON, email header, etc.)",
            default = [[First Name,Last Name,E-mail,Notes
FIRST,LAST,contact@example.com,VIP]]
        }
    },
    output = {
        contact_id = field.string{required = true},
    },
    function(input)
        importer({message = "Import this contact record:\n" .. input.raw_contact})

        assert(file_contact.called(), "Agent did not call file_contact")

        -- Prefer the tool return value, but fall back to deterministic derivation from args
        -- so this file remains testable in mock mode.
        local contact_id = file_contact.last_result()
        if type(contact_id) ~= "string" then
            local call = file_contact.last_call()
            local email = call and call.args and call.args.email
            assert(email, "file_contact was called, but email argument was missing")
            contact_id = "contact_" .. email
        end

        return {contact_id = contact_id}
    end
}

Specifications([[
Feature: Intro contact import
  Scenario: Agent files a contact
    Given the procedure has started
    When the procedure runs
    Then the file_contact tool should be called exactly 1 time
    And the output contact_id should match pattern "^contact_"
    And the procedure should complete successfully
]])
