git submodule init
git submodule update
mv -f ./shadowsocks/shadowsocks/* ./shadowsocks/
pyinstaller -y main.spec
