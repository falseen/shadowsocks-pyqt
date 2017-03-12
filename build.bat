rd /S /Q dist
git submodule init
git submodule update
move /Y .\shadowsocks\shadowsocks\* shadowsocks\
pyinstaller --distpath dist\files -y main.spec
pyinstaller -y main_onefile.spec
cd dist
mkdir shadowsocks_tmp
move shadowsocks-pyqt* shadowsocks_tmp\
xcopy /Y /I ..\res shadowsocks_tmp\res
copy /Y ..\config.json shadowsocks_tmp\
copy /Y ..\gui-config.json shadowsocks_tmp\
move shadowsocks_tmp shadowsocks-pyqt
cd ..
