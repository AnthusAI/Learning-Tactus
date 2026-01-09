-- Intro Example: Import One Contact (Give an Agent a Tool)
--
-- This is a runnable counterpart to the introduction’s code snippet.
-- It defines a local `file_contact` tool (as a stub) so the agent has a real capability to call.

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

input {
    raw_contact = field.string{
        required = true,
        description = "One contact record as raw text (CSV header+row, JSON, email header, etc.)",
        default = [[First Name,Last Name,E-mail,Notes
FIRST,LAST,contact@example.com,VIP]]
    }
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

output {
    contact_id = field.string{required = true},
}

importer({message = "Import this contact record:\n" .. input.raw_contact})

assert(file_contact.called(), "Agent did not call file_contact")

return {
    contact_id = file_contact.last_result()
}

Specifications([[
Feature: Intro contact import
  Scenario: Agent files a contact
    When the procedure runs
    Then the file_contact tool should be called
]])
