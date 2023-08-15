# rf-platform

射频功放平台

## Project setup

```
npm install

pip install
```

### Compiles and hot-reloads for development

```
# 先启动pyhton

npm run dev
```

### Compiles and minifies for production

```
pyinstaller --uac-admin -w -F rfplatformServe.py --distpath D:\Code\Vscode\rf-platform\dist_python --hidden-import=main

npm run electron:build

# 打包, 全部打包之后将该文件放在安装目录中  win-unpacked\python-serve下
```
