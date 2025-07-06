/bin/bash
sudo apt-get install cowsay -y
sudo apt-get install tree -y
cowsay -f dragon "my name is daenerys targaryen and my favorite dragon is DRogon" >> a-joke.txt
grep -i "dragon" a-joke.txt
ls -latr