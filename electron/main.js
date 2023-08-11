const { app, BrowserWindow, Menu, dialog, globalShortcut } = require('electron')
const path = require("path")

let mainWindow;

Menu.setApplicationMenu(null)

const createWindow = () => {
    // 创建浏览器窗口
    mainWindow = new BrowserWindow({
        // 默认窗口标题，如果由loadURL()加载的HTML文件中含有标签<title>，此属性将被忽略。
        title: "electron+vue+vite",
        width: 1000,
        height: 600,
        // 设置最小尺寸
        minWidth: 1000,
        minHeight: 600,
        // 窗口图标。 在 Windows 上推荐使用 ICO 图标来获得最佳的视觉效果, 默认使用可执行文件的图标.
        // 在根目录中新建 build 文件夹存放图标等文件
        icon: path.resolve(__dirname, "../build/icon/icon-20.ico"),
    });
    mainWindow.maximize()
    // 使用 loadURL 加载 http://localhost:9527 ，也就是 Vue 项目地址
    mainWindow.loadURL("http://localhost:9527/");

    // 如果使用了 nginx 代理，url 改为代理地址
    //   mainWindow.loadURL("https://example.com/");

    //打包
    // mainWindow.loadURL(`file://${path.join(__dirname, "../dist/index.html")}`);

    mainWindow.on("close", (e) => {
        e.preventDefault();
        dialog
            .showMessageBox(mainWindow, {
                type: "info",
                title: "退出提示",
                defaultId: 0,
                cancelId: 1,
                message: "确定要退出吗？",
                buttons: ["退出", "取消"],
            })
            .then((res) => {
                if (res.response === 0) {
                    // e.preventDefault();
                    // mainWindow.destroy();
                    app.exit(0);
                }
            });
    });
};

// 限制只能打开一个窗口
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
    app.quit();
} else {
    app.on("second-instance", () => {
        // 当运行第二个实例时,将会聚焦到 mainWindow 这个窗口
        if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore();
            mainWindow.focus();
            // mainWindow.show();
        }
    });

    // 在应用准备就绪时调用函数
    app.whenReady().then(() => {
        globalShortcut.register('Alt+D', function () {
            mainWindow.webContents.openDevTools()
        })
        createWindow();
        app.on("activate", () => {
            if (BrowserWindow.getAllWindows().length === 0) createWindow();
        });
    });
}

// 除了 macOS 外，当所有窗口都被关闭的时候退出程序。 因此，通常对程序和它们在任务栏上的图标来说，应当保持活跃状态，直到用户使用 Cmd + Q 退出。
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
