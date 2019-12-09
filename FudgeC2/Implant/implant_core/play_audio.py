class PlayAudio:
    type = "PS"
    args = "sound file location (on Fudge)"
    input = "play_audio"

    def process_implant_response(self):
        print("We're processing downloaded file")

    def implant_text(self):
        var = '''
function {{ ron.obf_remote_play_audio }}($data) {
    $args[0]
}
'''
        return var
