# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=[''],
             binaries=[],
             datas=[('res/Shadowsocks_logo.png', 'res'), ('config.json', '.'), ('gui-config.json', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='shadowsocks-pyqt',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='res/shadowsocks.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='shadowsocks-pyqt')

exe_debug = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='shadowsocks-pyqt_debug',
          debug=False,
          strip=False,
          upx=False,
          console=True , icon='res/shadowsocks.ico')

coll_debug = COLLECT(exe_debug,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='shadowsocks-pyqt_debug')