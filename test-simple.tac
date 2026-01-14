Procedure "main" {
    output = {
        message = field.string{required = true},
    },
    function(input)
        return {
            message = "Hello"
        }
    end
}
