pip install --user -r requirements.txt
sudo apt install python-dialog

mkdir -p ~/.config/gitclk
cp -a ./config ./scripts ~/.config/gitclk
chmod -R +x ~/.config/gitclk/scripts

ln -sfn ~/.config/gitclk/scripts/git_remotes_setting.py ~/.local/bin/gitclk-remotes
ln -sfn ~/.config/gitclk/scripts/github_repository_creation.sh ~/.local/bin/gitclk-create

git config --global alias.pushall "!git remote | xargs -L1 git push --all"
git config --global alias.pushalltags "!git remote | xargs -L1 git push --tags"