-- Procedure Skeleton (for docs)
-- Demonstrates the explicit Procedure { ... } wrapper shape.

-- snippet:start procedure-skeleton
Procedure {
    input = {
        name = field.string{required = true, description = "Name to greet"}
    },
    output = {
        greeting = field.string{required = true}
    },
    function(input)
        return {greeting = "Hello, " .. input.name .. "!"}
    end
}
-- snippet:end procedure-skeleton

Specifications([[
Feature: Procedure skeleton
  Scenario: Returns greeting
    Given the procedure has started
    When the procedure runs with param name="World"
    Then the procedure should complete successfully
    And the output greeting should match pattern "^Hello, "
]])

