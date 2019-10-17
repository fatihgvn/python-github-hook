# python-github-hook

## How to install

```
git clone git@github.com:fatihgvn/python-github-hook.git githubWebHook
cd githubWebHook/
mkdir -p logs
mkdir -p payloads
echo "{}" > hooks.json
```

## Add startup this hook server

Use the following command with root (for linux server)

```
(crontab -u $USER -l; echo "@reboot $PWD/autoRun.sh") | crontab -u $USER -
```
The crontab line should look like this
```
@reboot /root/githubWebHook/autoRun.sh
```
