# HashcatHerder

usage: HashcatHerder.py [-h] [-f Hash FILE] [-m MODE] [-p potfile] [-r]
                        [--dbcheck HASH] [--rulesOnly] [--rulesPlus]

optional arguments:
  -h, --help            show this help message and exit
  
  -f Hash FILE, 
  --hfile Hash FILE     File containing hashes
  
  -m MODE, 
  --mode MODE           Hash Type (Hashcat Mode ex:--mode=500)
  
  -p potfile, 
  --pFile potfile       Alternate potfile
  
  -r, 
  --rules               Run rules first, then Brute
  
  --dbcheck HASH        Check DB for hash ex: --dbcheck '5f4dcc3b5aa765d61d8327deb882cf99'
  
  --rulesOnly           Dont Brute, Only use rules
  
  --rulesPlus           Extended Rules then Brute


sudo python3 HashcatHerder.py -m 100 -f /passwords/hash2.txt --rulesOnly

[*] Starting Time 2019-02-26 22:53:25.964595
[+] Start File  : /passwords/hash2.txt
[+] Start Count : 32
[+] Mode        : 100
[+] Hash File   : /opt/hashERLoopER/working/log/hash2.txt_02272019_03_53_25
[+] Log File    : /opt/hashERLoopER/working/log/hash2.txt_02272019_03_53_25.log
[+] Pot File    : /opt/hashERLoopER/working/log/hash2.txt_02272019_03_53_25.pot
[*] Checking if Hashes are in DB
[*] Elapsed Time (hh:mm:ss.ms) 0:00:00.002474
[*] New Count   : 32
[+] Rules       : /mnt/NoName/PList/rules/ALL/
[*] Wordlist    : 10k-most-common.txt 1 out of 3
[+] Rule file   : toggles1.rule 1 out of 28
[+] Wordlist    : /mnt/NoName/PList/rules/ALL/10k-most-common.txt 
