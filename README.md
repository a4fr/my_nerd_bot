my_nerd_bot
------------
`my_nerd_bot` is a cute telegram bot that help you in every where. It return first lines of given word wikipedia's page. Also it has some funny CheatCode. CheatCode is a word or an expression that has a special define for `my_nerd_bot` (eg. tell bot `گشنمه` of `w shiraz`).


list of CheatCode and ReservedCode in this port
-------------------------------------------------
**CheatCodes:**
- `گشنمه` or `گرسنمه` or `غذای ایرانی`: with this words bot return you name of an iranian delicious food.
- `w <word>` or `wiki <wiki>` or `wiki_en`: return first lines of English wikipedia page of <word>.
- `عکس <word>`: if there are images in wikipedia pages of <word>, send you a random image.

**ReservedCode**
- `سلام`
- `خوبی؟`
- `ممنون`
- `خداحافظ`
- `کمک`
- `/help`
- `/start`
- `a4fr`


my_nerd_bot on RedHat openshift
--------------------------------
This branch port of my_nerd_bot telegram bot for run on RedHat openshift. OpenShift is Red Hat's Platform-as-a-Service (PaaS) that allows developers to quickly develop, host, and scale applications in a cloud environment. With OpenShift you have choice of offerings, including online, on premise, and open source project options ([learn more](https://www.openshift.com/products)).


Cartridges
-----------
You need to add this cartridges to run this port of my_nerd_bot:
- **python-3.3**
- **mongodb-2.4**


Run Bot
-------
- Edit `TOKEN` variable, `USERNAME` and `PASSWORD` in `rhc-nerd/bot/nerd_config.py`.
- Edit `USERNAME` and `PASSWORD` in `rhc-nerd/nerd_reporter`.
- Send files eith `git` on your openshift private repository.
- Then Login to you openshift app with `rhc ssh` and run bot with `python3.3 app_root/repo/bot/nerd_bot.py &`


Report and logs
----------------
All datas and logs stores in MongoDB. You can see this log in your web browser:
- **Logs:** `http://<your-app>-<openshift-id>.rhcloud.com/report/log`
- **List of CheatCodes:** `http://<your-app>-<openshift-id>.rhcloud.com/report/cheatcode`
- **List of ReservedCodes:** `http://<your-app>-<openshift-id>.rhcloud.com/report/reserved_code`



