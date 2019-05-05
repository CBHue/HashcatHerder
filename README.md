# HashcatHerder

![alt text](https://github.com/CBHue/HashcatHerder/blob/master/HashcatHerder.png)

This is a set it an forget it hashcat wrapper written in python3. 
it loops over a set of wordlists untill it cracks all the passwords or cycles thru all the wordlists. 

<pre>usage: HashcatHerder.py [-h] [--mode MODE] [-f Hash FILE]
                        [--addOn Add on Hashcat options] [-p potfile] [--mask]
                        [--brute] [--dbcheck HASH] [--rules] [--rulesPlus]
                        [--wordlist] [--hybrid] [--All]

optional arguments:
  -h, --help            show this help message and exit
  --mode MODE           Hashcat Mode
  -f Hash FILE, --hfile Hash FILE
                        Hash File
  --addOn Add on Hashcat options
                        All Attacks
  -p potfile, --pFile potfile
                        Alternate potfile
  --mask                Mask Attack ex: &apos;?a?a?a?a?a?a?a&apos;
  --brute               Brute-force &apos;?a?a?a?a?a?a?a&apos; incrementing
  --dbcheck HASH        Check DB for hash ex: --dbcheck
                        &apos;5f4dcc3b5aa765d61d8327deb882cf99&apos;
  --rules               Quick Rules only
  --rulesPlus           Extended Rules
  --wordlist            Wordlist Only
  --hybrid              Hybrid Attack
  --All                 All Attacks
</pre>

# Straight Mode - Just loop thru all the wordlists
sudo python3 HashcatHerder.py --mode 100 -f /passwords/hash2.txt --wordlist

# Rules Mode + Straight Mode - Loop thru a quick set of Rules then all the Wordlists.
sudo python3 HashcatHerder.py --mode 100 -f /passwords/hash2.txt --rules --wordlist

# All
<pre>sudo python3 /opt/HashcatHerder/HashcatHerder.py -f ./ALL-USERNAMES.HASH --mode 1000 --All --addOn=&apos;-O --username&apos;</pre>

# DBCheck
<pre>sudo python3 /opt/<font color="#EF2929"><b>Hash</b></font>catHerder/<font color="#EF2929"><b>Hash</b></font>catHerder.py --dbcheck ntds.hashes</pre>
