-- State API Examples (for docs)
-- These snippets are used in the State Management chapter.

Procedure {
    output = {
        ok = field.boolean{required = true}
    },
    state = {
        items_processed = field.number{default = 0},
        attempts = field.number{default = 0},
        events = field.array{default = {}},
        message_id = field.string{description = "Example idempotency marker"}
    },
    function(input)
        -- snippet:start state-set-get
        -- Set
        state.items_processed = 0

        -- Get
        local n = state.items_processed

        -- Check for existence / truthiness
        if state.message_id then
          Log.info("Already sent", {message_id = state.message_id})
        end
        -- snippet:end state-set-get

        -- snippet:start state-helpers
        State.increment("attempts")        -- attempts += 1
        State.increment("attempts", 5)     -- attempts += 5
        State.append("events", "drafted")  -- append to a list
        local snapshot = State.all()       -- dump all state
        -- snippet:end state-helpers

        return {ok = n == 0 and snapshot ~= nil}
    end
}

Specifications([[
Feature: State API examples
  Scenario: Demonstrates state helpers
    Given the procedure has started
    When the procedure runs
    Then the procedure should complete successfully
]])

