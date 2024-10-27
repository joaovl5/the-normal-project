// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain } = require("electron");
const { initialize, enable } = require("@electron/remote/main");

const path = require("node:path");
// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

initialize();

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 642 * 1.5,
    height: 394 * 1.5,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true,
      sandbox: false,
      preload: path.join(__dirname, "preload.js"),
    },
    autoHideMenuBar: true,
    resizable: false,
  });

  enable(mainWindow.webContents);

  mainWindow.loadURL("http://localhost:9965/index.html");
}

ipcMain.on("do-something", (event, args) => {
  console.log("Doing something", args);
});

app.on("ready", createWindow);

app.on("window-all-closed", function () {
  app.quit();
});

app.on("activate", function () {
  if (mainWindow === null) createWindow();
});
