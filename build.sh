rm -rf ./dist/*
git submodule init
git submodule update
mv -f ./shadowsocks/shadowsocks/* ./shadowsocks/
pyinstaller --distpath dist/files -y main.spec
pyinstaller -y main_onefile.spec
cd dist
mkdir shadowsocks_tmp
mv shadowsocks-pyqt* shadowsocks_tmp/
cp -a -f ../res shadowsocks_tmp/
cp -f ../config.json shadowsocks_tmp/
cp -f ../gui-config.json shadowsocks_tmp/
mv shadowsocks_tmp shadowsocks-pyqt
cd ..
