
def banner():                                                           
	print("\033[91m{}\033[00m" .format("""  
                                                                                                                   
,--.  ,--.                  ,--.                        ,--.   ,--.  ,--.                    ,--.                 
|  '--'  |  ,--,--.  ,---.  |  ,---.   ,---.  ,--,--. ,-'  '-. |  '--'  |  ,---.  ,--.--.  ,-|  |  ,---.  ,--.--. 
|  .--.  | ' ,-.  | (  .-'  |  .-.  | | .--' ' ,-.  | '-.  .-' |  .--.  | | .-. : |  .--' ' .-. | | .-. : |  .--' 
|  |  |  | \ '-'  | .-'  `) |  | |  | \ `--. \ '-'  |   |  |   |  |  |  | \   --. |  |    \ `-' | \   --. |  |    
`--'  `--'  `--`--' `----'  `--' `--'  `---'  `--`--'   `--'   `--'  `--'  `----' `--'     `---'   `----' `--' 
"""))

def printC(out): print("\033[96m{}\033[00m" .format("[-] " + out)) 

def title():
    print("------------------------------------------------------------------------------------------------------")
    printC("Tool      : HashcatHerder")
    printC("Author    : cbHu3")
    printC("Twitter   : @_cbhue_")
    printC("github    : https://github.com/CBHue")
    print("------------------------------------------------------------------------------------------------------")
    print("")