const { contextBridge, ipcRenderer } = require("electron");
const { BrowserWindow } = require("@electron/remote");

contextBridge.exposeInMainWorld("myWindowAPI", {
  minimize() {
    BrowserWindow.getFocusedWindow().minimize();
  },

  toggleMaximize() {
    const win = BrowserWindow.getFocusedWindow();

    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.maximize();
    }
  },

  close() {
    BrowserWindow.getFocusedWindow().close();
  },

  show() {
    BrowserWindow.getFocusedWindow().show();
  },

  hide() {
    BrowserWindow.getFocusedWindow().hide();
  },
});

console.log("BUG BUG");
