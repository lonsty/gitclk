pip install --user -r requirements.txt
sudo apt install python-dialog

mkdir -p ~/.config/git-clk
cp -a ./config ./scripts ~/.config/git-clk
chmod -R +x ~/.config/git-clk/scripts

sudo ln -sfn ~/.config/git-clk/scripts/git_remotes_setting.py /usr/local/bin/gitclk-remotes
sudo ln -sfn ~/.config/git-clk/scripts/github_repository_creation.sh /usr/local/bin/gitclk-create