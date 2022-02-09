This is a Old Yukki Music source code, Check out the new version here: https://github.com/NotReallyShikhar/YukkiMusicBot

Credit for [@TeamYukki](https://t.me/OfficialYukki) as the owner & creator of this Repository.

### String Session

[![GenerateString](https://img.shields.io/badge/repl.it-generateString-yellowgreen)](https://replit.com/@levinalab/Session-Generator?lite=1&outputonly=1#main.py)

Generate & Choose pyrogram session string for session var.

### Deploy To Heroku 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

This repo has blacklisted by Heroku, to deploy this repo you need to fork this repo first by pressing the fork button in the upper right corner of this page and then clicking the deploy button above.

## VPS Deployment 📡
Get the best Quality of streaming performance by hosting it on VPS, here's the step's:

```sh
sudo apt update && apt upgrade -y
sudo apt install git curl python3-pip ffmpeg -y
pip3 install -U pip
curl -sL https://deb.nodesource.com/setup_16.x | bash -
sudo apt-get install -y nodejs
npm i -g npm
git clone https://github.com/levina-lab/YukkiMusic-Old # clone the repo.
cd YukkiMusic-Old
pip3 install -U -r requirements.txt
cp sample.env .env # use vim to edit ENVs
vim .env # fill up the ENVs (Steps: press i to enter in insert mode then edit the file. Press Esc to exit the editing mode then type :wq! and press Enter key to save the file).
python3 -m Yukki # run the bot.

# continue the host with screen or anything else, thanks for reading.
```
