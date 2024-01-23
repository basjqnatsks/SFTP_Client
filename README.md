# SFTP_Client
SFTP client that connects to SFTP server and downloads files from folder to specified folder




sftp_client.py
    Commands:
            Layout:
                    python sftp_client.py IP(STR) USERNAME(STR) PASSWORD(STR) LOCATION(STR)
            Required:  
                IP(STR):
                    IP for server
                    example sftp.paycomonline.net
                USERNAME(STR):
                PASSWORD(STR):
                
            Optional:  
                FOLDER LOCATION(STR):
                    If empty program will default to local folder.

            example python stfp_client.py "1.1.1.1" "root" "pass"  "C:\Users\User\Desktop\Files"
