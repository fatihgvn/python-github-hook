# python-github-hook

## How to install

```
git clone git@github.com:fatihgvn/python-github-hook.git githubWebHook
cd githubWebHook/
mkdir -p logs
mkdir -p payloads
echo "{}" > hooks.json
```

## Add hook server to startup

Use the following command with root (for linux server)

```
(crontab -u $USER -l; echo "@reboot $PWD/autoRun.sh") | crontab -u $USER -
```
The crontab line should look like this
```
@reboot /root/githubWebHook/autoRun.sh
```
## How to add new WebHook

Go to `settings> webhooks` in your repository.
Click the 'Add WebHook' button.
This project runs on port `8181` by default. Enter your IP address or domain name and add `:8181`.
It should be like `http://exampleserver.com:8181`.
Select content type is `application/json` and submit the form.

When you submit the form, the request is sent to your server and your server downloads this project in the tmp directory by default.

Open `hooks.js`, edit the location of the last added id, and move the files in the tmp folder to that location.