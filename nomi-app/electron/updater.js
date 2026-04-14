const { autoUpdater } = require('electron-updater')
const { BrowserWindow } = require('electron')

autoUpdater.autoDownload = false
autoUpdater.autoInstallOnAppQuit = true

function setupUpdater(win) {
  autoUpdater.checkForUpdates().catch(() => {
    // silencioso en dev
  })

  autoUpdater.on('update-available', (info) => {
    win.webContents.send('update-available', info.version)
    autoUpdater.downloadUpdate()
  })

  autoUpdater.on('update-downloaded', () => {
    win.webContents.send('update-downloaded')
  })
}

module.exports = { setupUpdater }
