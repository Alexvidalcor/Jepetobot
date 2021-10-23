
# [En desarrollo] YoutubeBOT

_Bot de Telegram que, de momento, sólo cuenta suscriptores en un canal de Youtube._

_Se incluye soporte para despliegue en AWS_


## Comenzando 🚀

_Para SO basados en Debian y Fedora._

Ver **Despliegue** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_Acceso a los recursos del repositorio:_

```
git clone https://github.com/Alexvidalcor/TelegramBot_YT

cd TelegramBot_YT/
```


## Ejecución del programa 🚀

### Instalación Distribución de Linux basada en Debian 

_Pasos a seguir (comandos de terminal):_

```
git clone https://github.com/Alexvidalcor/ExamMaker
cd ExamMaker/
python3 src/install.py
./execute.sh
```

## Despliegue 📦

**Deploy en local:**

Ejecutar el archivo "EnvCreate.py" para implementar un entorno virtual de Python con las dependencias necesarias (a través de "requirements.txt").

Para desactivar el entorno de Python generado:

```
deactivate
```

**Deploy en AWS (rama AWS del repositorio) [EN DESARROLLO - NO SE RECOMIENDA SU USO DE MOMENTO]:**

Necesario tener CDK preinstalado.

Dentro del directorio "AWS_IaC", modificar los stacks de "tel_bot_aws_stack.py" como se desee. Posteriormente ejecutar:

```
cdk synth

cdk deploy
```

**Para deploy manual en AWS (EC2 con AMI de "Amazon Linux 2")**

Ejecutar los siguientes comandos en la instancia EC2:

_Instalación de Google Chrome (Gracias a [UnderstandingData](https://understandingdata.com/install-google-chrome-selenium-ec2-aws/))_

```
sudo curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
```

_Comprobación de instalación_

```
google-chrome – version && which google-chrome
```

_Instalación de Python3 y librerías necesarias_

```
sudo yum install python3

sudo pip3 install python-telegram-bot
sudo pip3 install selenium
sudo pip3 install webdriver-manager
```


## Construido con 🛠️

* [AWS-CDK](https://aws.amazon.com/es/cdk/) - Despliegue en AWS.
* [Python-Telegram-Bot](https://python-telegram-bot.org) - API Wrapper de Telegram.
* [Selenium](https://www.selenium.dev/) - Web Scrapping.


## Licencia 📄

Este proyecto está bajo la Licencia (GNU GPL-V3) - mira el archivo [LICENSE.md](LICENSE.md) para detalles.


---
⌨️ con ❤️ por [Alexvidalcor](https://github.com/Alexvidalcor) 😊
