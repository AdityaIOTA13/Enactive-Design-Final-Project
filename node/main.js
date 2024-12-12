const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')
try {
    require('electron-reloader')(module, {
        ignore: ["output.png", "output.scad"]
    })
} catch (_) {}

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration:  true,
            contextIsolation: false,
        }
    })

    win.loadFile('index.html')
}

app.whenReady().then(() => {
    createWindow()
})

ipcMain.handle('load-image', async (event, imagePath) => {
    const image = fs.readFileSync(imagePath).toString('base64')
    return `data:image/png;base64,${image}`
})