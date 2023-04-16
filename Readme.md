
**CURRENT STATUS: STABLE**

<br><kbd>
<br><img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-logo1.png" width="500" />
</kbd><br>

_Telegram bot developed to explore the AI possibilities of OpenAI._

_Support for deployment on AWS is included through Github Actions._

_**This branch is used to develop new features**_

<br>

## Main features :fire:


### AWS cloud support.

* IaC (Infrastructure as Code) support for cloud infrastructure on Amazon Web Services is included through the <ins>AWS CDK</ins>.

* <ins>Github Codespaces</ins> support is included (see [devcontainer](https://github.com/Alexvidalcor/jepetobot/blob/master/.devcontainer/devcontainer.json))

* Support for local execution is also included.


### Automated deployment of cloud infrastructure and code.

* The deployment of cloud infrastructure on AWS has been automated through <ins>Github Actions</ins>.

* New code releases have also been automated via Github Actions and <ins>Docker containers</ins>.


### Easy access to ChatGPT (GPT3.5-turbo) from Telegram

Adapted to the latest chatgpt model | 'Identity' change from bot options | 'Temperature' change from bot options
--- | --- | --- |
 | <img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-image1.gif" height="400" width="200"/> | <img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-image2.gif" height="400" width="200"/> | <img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-image3.gif" height="400" width="200"/> |
 

### Management system of users

* A system has been added to enable or deny access to specific user IDs

* The user management system can also be applied to the configuration access.


### Support for conversations

* The bot remembers the conversations of each user

* It is allowed to delete the stored conversations easily from the bot settings.


### Statistics enabled

* A statistics function has been implemented that allows more control over the behavior of the application.

* This feature complements an advanced monitoring system.

<br>

## Getting started 🚀

As the entire infrastructure is automated in the cloud, <ins>it is not necessary to install anything locally</ins>. You only need to have the following:

<br><kbd>
<br><img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-started1.png" height="100" width="200"/>
</kbd><br>

* The Github account is necessary to fork the code and to be able to execute the [deployment automations](https://github.com/Alexvidalcor/jepetobot/tree/master/.github/workflows)

* To create an account on Github, go to the [official website](https://github.com/) and follow the steps described there.

<br><kbd>
<br><img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-started2.png" height="100" width="200"/>
</kbd><br>

* Obviously, you need a Telegram account to deploy a bot on Telegram.

* To create a Telegram account, you must download a Telegram client and follow the steps described there.

* It is necessary to obtain a token from the Telegram Bot API.

* Instructions for it are [HERE](https://core.telegram.org/bots#how-do-i-create-a-bot).

<br><kbd>
<br><img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-started3.png" height="80" width="200"/><br><br>
</kbd><br>

* All the infrastructure of the application is deployed in AWS, therefore, an account is needed in said public cloud provider to be able to create the necessary resources.

* You can see how to create an AWS account [HERE](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)

* It is necessary to obtain a Access Key and a Secret Access Key from the AWS Management Console.

* Instructions for it are [HERE](https://repost.aws/knowledge-center/create-access-key)

<br><kbd>
<br><img src="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-started4.png" height="60" width="200"/><br><br>
</kbd><br>
 
* The main functionality of Jepetobot is based on the OpenAi api, therefore an account is needed there.

* To create an OpenAi account, you can click [HERE](https://auth0.openai.com/u/signup/)

* It is necessary to obtain a token from the OpenAI API.

* Instructions for it are [HERE](https://platform.openai.com/docs/introduction/tokens).

<br>

| :exclamation:  If you already have the above, check the [Wiki](https://github.com/Alexvidalcor/jepetobot/wiki/How-To-Use) for <ins>step by step usage guide</ins>  |
|-----------------------------------------|

<br>

## Cloud deployment overview :cloud:


Currently there are two Github Actions workflows prepared to automate the cloud deployment:


* _[cdk_deploy_resources.yaml](https://github.com/Alexvidalcor/jepetobot/blob/master/.github/workflows/deploy_resources.yaml)_

Resources | EC2 | S3| secretmanager | codedeploy | cloudwatch |
--- | --- | --- | --- | --- | --- |
Purpose | Machine where the application is hosted | Bucket where application versions are stored | Secret Manager inside AWS | Automates the deployment of new versions of the application | Monitor logs easily |


* _[update_application.yaml](https://github.com/Alexvidalcor/jepetobot/blob/master/.github/workflows/update_application.yaml)_

Update cloud app code with every push to master branch. It generates a slight service downtime of a few seconds.

<br>

| :zap:        All use of cloud and OpenAi api generate costs, use it at your own risk!   |
|-----------------------------------------|

<br>

## Built with 🛠️

* [AWS-CDK](https://aws.amazon.com/es/cdk/) - Deploy on AWS.
* [Python-Telegram-Bot](https://python-telegram-bot.org) - Telegram Api Wrapper.
* [OpenAI-Api](https://openai.com/api/) - AI api

<br>

## Disclaimer :memo:

* I'm not responsible for bricked devices or software misconfigurations.
* I'm not responsible for possible high cloud costs/openai api costs generated by using the code of this project.
    * **You are free to use the software of this project and it is your decision**. As I explain in the [wiki](https://github.com/Alexvidalcor/jepetobot/wiki), this project originates from an experiment and fully stable operation is not guaranteed.
* I'm not responsible for data loss.

This is a personal project with academic origins and is not intended to be a commercial or professional solution. If you want to use it, it is at your own risk.

<br>

## Roadmap :spiral_calendar:

| :exclamation:  Check the [Project dashboard](https://github.com/users/Alexvidalcor/projects/2) for more info!  |
|-----------------------------------------|

<br>

## Wiki :closed_book:

| :exclamation:  Check the [Wiki](https://github.com/Alexvidalcor/jepetobot/wiki) for more info!  |
|-----------------------------------------|

<br>

## License :pushpin:

This project is licensed under the License (GNU GPL-V3) - see the [LICENSE.md](LICENSE.md) file for details.



---

⌨️ with ❤️ by [Alexvidalcor](https://github.com/Alexvidalcor) 😊
