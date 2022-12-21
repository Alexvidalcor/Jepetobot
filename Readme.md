
# [DEVELOPING BRANCH] [DONT USE] TelegramBot

_Bot de Telegram que, de momento, sólo cuenta suscriptores en un canal de Youtube._

_Se incluye soporte para despliegue en AWS_


## Ejecución del programa 🚀

### Distribución de Linux basada en Debian 

_Instalación Manual (comandos de terminal):_

```
git clone https://github.com/Alexvidalcor/TelegramBot
cd TelegramBot/
python3 src/installation/install.py
./src/installation/execute.sh
```

_Instalación mediante Docker (se requiere tener Docker instalado previamente):_
```
git clone https://github.com/Alexvidalcor/TelegramBot
docker build -t telegrambot . 
docker run -d -it --name telegrambot_cont telegrambot
```


## Despliegue 📦

**Deploy en AWS (dentro de carpeta cdk) [EN DESARROLLO - NO SE RECOMIENDA SU USO]:**

Necesario tener CDK preinstalado. Ejecutar:

```
cdk synth

cdk deploy --all
```

## Construido con 🛠️

* [AWS-CDK](https://aws.amazon.com/es/cdk/) - Despliegue en AWS.
* [Python-Telegram-Bot](https://python-telegram-bot.org) - API Wrapper de Telegram.
* [Selenium](https://www.selenium.dev/) - Web Scrapping.


## Licencia 📄

Este proyecto está bajo la Licencia (GNU GPL-V3) - mira el archivo [LICENSE.md](LICENSE.md) para detalles.


---
⌨️ con ❤️ por [Alexvidalcor](https://github.com/Alexvidalcor) 😊

..