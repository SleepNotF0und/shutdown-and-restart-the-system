import os
ch = int(input("Press 1 to Shutdown || Press 2 to Restart\n>>"))
if ch == 1:
    os.system("shutdown /s /t 1")
elif ch ==2:
    os.system("shutdown /r /t 1")
else:
    exit()