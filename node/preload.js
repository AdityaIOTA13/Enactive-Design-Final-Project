const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
    loadImage: (imagePath) => ipcRenderer.invoke('load-image', imagePath)
})