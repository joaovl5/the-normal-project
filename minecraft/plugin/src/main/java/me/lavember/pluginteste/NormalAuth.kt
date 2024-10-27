package me.lavember.pluginteste

import org.bukkit.plugin.java.JavaPlugin

class NormalAuth : JavaPlugin() {
    companion object {
        lateinit var instance: NormalAuth private set
        lateinit var loginProcess: LoginProcess private set
        lateinit var authService: AuthService private set
    }

    override fun onEnable() {
        instance = this
        loginProcess = LoginProcess()
        authService = AuthService()

        logger.info("AVISO FODASE BUBGUBG")
        server.pluginManager.registerEvents(JoinListener(), this)
        this.getCommand("login")?.setExecutor(LoginCommand())

    }

    override fun onDisable() {
        // Plugin shutdown logic
    }


}
