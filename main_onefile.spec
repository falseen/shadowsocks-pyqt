# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=[''],
             binaries=[],
             datas=[('res/Shadowsocks_logo.png', 'res')],
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
          a.datas,
          a.scripts,
          a.binaries,
          a.zipfiles,
          name='shadowsocks-pyqt',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='res/shadowsocks.ico')
