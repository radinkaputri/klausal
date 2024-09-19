# Deploy to HEROKU

**<u>Important Note:</u>**
1. Add all of your private files here: `config.env`, `token.pickle`, `rcl.conf`, `accounts.zip`, `shorteners.txt` etc...

**<u>Mandatory Veriables in Config:</u>**

- `UPSTREAM_REPO`: Your github repository link, if your repo is private add `https://<deploy_token>:<empty_password>@gitlab.com/<your_username>/<repository_name>
` format. `Str`.
  - **NOTE**: Don't forget to remove '<' and '>' . Follow [**THIS TUTORIAL**](https://graph.org/GitLab-Upstream-Tutorial-06-02) to generate upstream repo. 
              - Any change in docker or requirements you need to deploy/build again with updated repo to take effect. 
              - **DON'T delete .gitignore file**. For more information read [**THIS**](https://github.com/Dawn-India/Z-Mirror#upstream-repo-recommended).
- `UPSTREAM_BRANCH`: Upstream branch for update. Default is `upstream`. `Str`

- `BOT_TOKEN`: The Telegram Bot Token that you got from [**BotFather**](https://t.me/BotFather). `Str`
- `OWNER_ID`: The Telegram User ID (not username) of the Owner of the bot. `Int`
- `TELEGRAM_API`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from **<https://my.telegram.org>**. `Int`
- `TELEGRAM_HASH`: This is to authenticate your Telegram account for downloading Telegram files. You can get this from **<https://my.telegram.org>**. `Str`

- `BASE_URL`: Add a valid `BASE URL` to use torrent selection. Copy it from your heroku app. Right click on `OPEN APP` and copy link address. Format of URL should be `https://APPNAME-IDENTIFIER.herokuapp.com/`, where `APPNAME` is the name of your heroku app and IDENTIFIER is an unic number. Example: `https://ZeeApp1-mjw69x6ex696.herokuapp.com/`. `Str`
- `TORRENT_TIMEOUT`: Timeout of dead torrents downloading with qBittorrent and Aria2c in seconds. `Int`

---
### For farther assistance visit my support group: [**@Z_Mirror**](https://telegram.me/z_mirror).
---

## Deploy using CLI

- Deployment instructions uploaded [**HERE**](https://gist.github.com/Dawn-India/9be1ca66b392dee82bcbc8d7f7ebefe8)
- Carefully copy-paste every CMD one by one. If you miss maybe your BOT will not run.

## Deploy using Google Colab

- Visit this [**LINK**](https://free.cyberurl.in/0vx4s) and follow on-screen instructions.

---
### Demo BOT available here: [**@Z_Mirror**](https://telegram.me/z_mirror).
---