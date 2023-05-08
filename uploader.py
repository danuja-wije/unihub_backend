from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder = "18_Kr0PneuKorEAdSqXJ8ijtZN27qTX1R"

# file1 = drive.CreateFile({'parents':[{'id':folder}],'title':'avatar.png'})

# file1.SetContentString()