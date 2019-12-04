pip uninstall -y pythondialog
sudo apt purge python-dialog python3-dialog -y

sudo rm -f /usr/local/bin/gitclk-remotes /usr/local/bin/gitclk-create
rm -rf ~/.config/gitclk

git config --global --unset alias.pushall
git config --global --unset alias.pushalltags