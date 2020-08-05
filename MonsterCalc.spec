# -*- mode: python -*-

block_cipher = None


a = Analysis(['MonsterCalc.py'],
             pathex=['C:\\Users\\acarro12\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\PySide2', 'C:\\GitHub\\MonsterCalc'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MonsterCalc',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='C:\\GitHub\\MonsterCalc\\Monster.ico')
