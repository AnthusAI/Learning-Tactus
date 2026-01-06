-- code/chapter-02/deployment-agent.tac
-- Demonstrates durable execution with human-in-the-loop approval

Tool "done" {
    description = "Signal that deployment preparation is complete",
    input = {
        changes = field.string{required = true, description = "Summary of changes"}
    },
    function(args)
        return args.changes
    end
}

Agent "deployer" {
    provider = "openai",
    model = "gpt-4o",
    system_prompt = [[You are a deployment assistant. Your job is to:
1. Review the changes to be deployed
2. Identify any risks or concerns
3. Prepare a deployment summary
4. Call the done tool with your summary when ready]],
    toolsets = {"done"}
}

Procedure "main" {
    input = {
        version = field.string{required = true, description = "Version to deploy"},
        environment = field.string{default = "staging", description = "Target environment"}
    },
    output = {
        deployed = field.boolean{required = true},
        summary = field.string{required = true}
    },
    function(input)
        Log.info("Preparing deployment", {
            version = input.version,
            environment = input.environment
        })

        -- Agent prepares deployment (survives crashes)
        repeat
            Agent("deployer").turn()
        until Tool.called("done")

        local changes = Tool.last_call("done").args.changes

        -- Human approval gate (can take hours)
        local approved = Human.approve({
            message = "Deploy " .. input.version .. " to " .. input.environment .. "?",
            context = {
                changes = changes,
                environment = input.environment
            }
        })

        if approved then
            Log.info("Deployment approved, proceeding")
            return {
                deployed = true,
                summary = "Deployed " .. input.version .. ": " .. changes
            }
        else
            Log.info("Deployment rejected")
            return {
                deployed = false,
                summary = "Deployment cancelled by reviewer"
            }
        end
    end
}

Specifications([[
Feature: Deployment with Approval

  Scenario: Deployment is prepared and awaits approval
    Given the procedure has started
    When the deployer agent takes turns
    Then the done tool should be called exactly once
]])
