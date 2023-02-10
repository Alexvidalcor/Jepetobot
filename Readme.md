
# [DEVELOPING BRANCH] TelegramBot

_Telegram bot developed to explore the AI possibilities of OpenAI_

_Support for deployment on AWS is included through Github Actions_


## Program execution 🚀

### Debian-based Linux distribution 

_Manual Installation (terminal commands):_

```
git clone https://github.com/Alexvidalcor/TelegramBot
cd TelegramBot/
python3 src/installation/install.py
./src/installation/execute.sh
```

_Installation using Docker (it is required to have Docker installed previously):_

```
git clone https://github.com/Alexvidalcor/TelegramBot
cd TelegramBot/
docker build -t telegrambot . 
docker run -d -it --name telegrambot_cont telegrambot
```


## Deployment 📦

**Deploy in AWS (inside cdk folder):**

Need to have CDK pre-installed. Execute:

```
cdk synth

cdk deploy --all
```


## Built with 🛠️

* [AWS-CDK](https://aws.amazon.com/es/cdk/) - Deploy on AWS.
* [Python-Telegram-Bot](https://python-telegram-bot.org) - Telegram Api Wrapper.


## License 📄

This project is licensed under the License (GNU GPL-V3) - see the [LICENSE.md](LICENSE.md) file for details.


---

⌨️ con ❤️ por [Alexvidalcor](https://github.com/Alexvidalcor) 😊

...