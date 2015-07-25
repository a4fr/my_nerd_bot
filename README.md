my_nerd_bot
------------
`my_nerd_bot` is a cute telegram bot that help you in every where. It return first lines of given word wikipedia's page. Also it has some funny CheatCode. CheatCode is a word or an expression that has a special define for `my_nerd_bot` (eg. tell bot `گشنمه` of `w shiraz`).
Start chat with `my_nerd_bot` in telegram web version http://telegram.me/my_nerd_bot .


list of CheatCode and ReservedCode in this port
-------------------------------------------------
**CheatCodes:**
- `گشنمه` or `گرسنمه` or `غذای ایرانی`: with this words bot return you name of an iranian delicious food.
- `w <word>` or `wiki <wiki>` or `wiki_en`: return first lines of English wikipedia page of <word>.

**ReservedCode**
- `سلام`
- `خوبی؟`
- `ممنون`
- `خداحافظ`
- `کمک`
- `/help`
- `/start`
- `a4fr`
- ...


my_nerd_bot on Google App Engine
--------------------------------
This branch port of my_nerd_bot telegram bot for run on Google App Engine. Google App Engine (often referred to as **GAE** or simply **App Engine**) is a platform as a service (**PaaS**) cloud computing platform for developing and hosting web applications in Google-managed data centers. Applications are sandboxed and run across multiple servers.
This port use **webhook** api.



Run Bot
-------
- Edit `TOKEN` variable in `nerd_config.py`.
- Deploy files with `appcnfg.py` on your Google App Engine.

logs
----------------
I use `logging` module for log `in_log` and `out_log`s. You can see logs in https://console.developers.google.com/project/your-project-name/logs .


webhook
---------
Google close SSL socket for free accounts. I chage some functions and https requests method in `telebot` and `wikipedia`. Until now this changes does not merge in original repository. Please use this files and don't change them with original modules. 

Comparare with my_nerd_bot for openshift
------------------------------------------------
- Has a better performance because of **webhook**.
- Just sent text, in future fix this problem.
- Has a dictionray and use `logging` instead of an external DataBase.






