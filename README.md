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

sudo python3 HashcatHerder.py -m 100 -f /passwords/hash2.txt

sudo python3 HashcatHerder.py -m 100 -f /passwords/hash2.txt --rulesOnly

sudo python3 HashcatHerder.py -m 100 -f /passwords/hash2.txt --rulesPlus
