# -*- mode: python -*-

block_cipher = None


a = Analysis(['fMain.py'],
             pathex=['C:\\Program Files (x86)\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'D:\\+myLinks\\Projects\\Python\\TelephoneBook\\forVlad'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PhoneBook',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='appIcon.ico')
