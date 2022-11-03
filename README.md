# Numbers_techtest
Firstly, you need to create telegram bot. command **/newbot** to @BotFather in Telegram.
It will create a new bot and give you its Token

Then create Google service account,generate json-key file. Call it **credentials.json** and place it to the working directory

After that, you need to create **tg_config.py**.
In **tg_config.py** create two variables:
  * **TGBOT_TOKEN**, string which is your bot's Token
  * **CHAT_ID**, string which is an id of a chat or a person you want to send message to

In order to program to work you need PostgreSQL installed on your computer

run **docker build -t <image_name> .** to build a docker image

run **docker run -d --name <container_name> -p 5432:5432 image_name**

Link to the Google sheets: 
https://docs.google.com/spreadsheets/d/1ApmXsn_QfVVIozsHrLNEozPuYzefp9bnH4ife1BINms/edit#gid=0
