
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


### Instalación 🔧

_Pasos para instalación de entorno y ejecución de programa._

* Caso distribuciones basadas en Debian:

```
python3 EnvCreate.py
```

* Caso Fedora:
```
python EnvCreate.py
```

_Activar el entorno Python generado:_

```
source <NombreEntorno>/bin/activate
```
_Ejecución del programa._

* Caso distribuciones basadas en Debian:

```
python3 main.py
```

* Caso Fedora:

```
python main.py
```


## Despliegue 📦

**Deploy en local:**

Ejecutar el archivo "EnvCreate.py" para implementar un entorno virtual de Python con las dependencias necesarias (a través de "requirements.txt").

Para desactivar el entorno de Python generado:

```
deactivate
```

**Deploy en AWS (necesario tener CDK preinstalado) [EN DESARROLLO - NO SE RECOMIENDA SU USO DE MOMENTO]:**

Dentro del directorio "AWS_IaC", modificar los stacks de "tel_bot_aws_stack.py" como se desee. Posteriormente ejecutar:

```
cdk synth

cdk deploy
```


## Construido con 🛠️

* [AWS-CDK](https://aws.amazon.com/es/cdk/) - Despliegue en AWS.
* [Python-Telegram-Bot](https://python-telegram-bot.org) - API Wrapper de Telegram.
* [Selenium](https://www.selenium.dev/) - Web Scrapping.


## Licencia 📄

Este proyecto está bajo la Licencia (GNU GPL-V3) - mira el archivo [LICENSE.md](LICENSE.md) para detalles.


---
⌨️ con ❤️ por [Alexvidalcor](https://github.com/Alexvidalcor) 😊