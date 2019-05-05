# HashcatHerder

![alt text](https://github.com/CBHue/HashcatHerder/blob/master/HashcatHerder.png)

This is a set it an forget it hashcat wrapper written in python3. 
it loops over a set of wordlists untill it cracks all the passwords or cycles thru all the wordlists. 

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

# Straight Mode - Just loop thru all the wordlists
sudo python3 HashcatHerder.py --mode 100 -f /passwords/hash2.txt --wordlist

# Rules Mode + Straight Mode - Loop thru a quick set of Rules then all the Wordlists.
sudo python3 HashcatHerder.py --mode 100 -f /passwords/hash2.txt --rules --wordlist

# All
<pre>sudo python3 /opt/HashcatHerder/HashcatHerder.py -f ./ALL-USERNAMES.HASH --mode 1000 --All --addOn=&apos;-O --username&apos;</pre>

# DBCheck
<pre>sudo python3 /opt/<font color="#EF2929"><b>Hash</b></font>catHerder/<font color="#EF2929"><b>Hash</b></font>catHerder.py --dbcheck ntds.hashes</pre>
