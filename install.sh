pip install --user -r requirements.txt
sudo apt install python-dialog

mkdir -p ~/.config/git-remotes-setting
cp -a ./config git_remotes_setting.py ~/.config/git-remotes-setting
chmod +x ~/.config/git-remotes-setting/git_remotes_setting.py

sudo ln -sfn ~/.config/git-remotes-setting/git_remotes_setting.py /usr/local/bin/git-remotes