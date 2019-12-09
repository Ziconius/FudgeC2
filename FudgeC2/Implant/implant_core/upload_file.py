class UploadFile:
    type = "FU"
    args = "base64-file::filelocation"
    input = "upload_file"

    def process_implant_response(self):
        print("We're processing uploaded file")

    def implant_text(self):
        var = '''
# Uploading files to client - Not yet implemented
function {{ ron.obf_upload_file }} () {}
'''
        return var
