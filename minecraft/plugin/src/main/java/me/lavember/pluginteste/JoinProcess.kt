package me.lavember.pluginteste

import org.bukkit.Location
import org.bukkit.entity.Player
import org.bukkit.potion.PotionEffect
import org.bukkit.potion.PotionEffectType

class JoinProcess(private val player: Player) {
    private val authy = NormalAuth.instance
    private val loginProcess = NormalAuth.loginProcess

    fun run() {
        PreLoginDataStore.save(player)
        joinTeleports()
        loginProcess.addPlayer(player)
        player.addPotionEffect(PotionEffect(PotionEffectType.BLINDNESS, Int.MAX_VALUE, 255))
        setTimeout()
    }

    private fun joinTeleports() {
        val x = 0.0
        val y = 5000 + 0.1
        val z = 0.0
        val yaw = 0.0f
        val pitch = 0.0f
        val world = "world"
        player.teleport(Location(NormalAuth.instance.server.getWorld(world), x, y, z, yaw, pitch))
    }

    private fun setTimeout() {
        val checkTask = authy.server.scheduler.runTaskLater(authy, Runnable {
            if(loginProcess.contains(player)) {
                player.kickPlayer("PODE IR SAINDO! DEMOROU DEMAIS PRA LOGAR TROUXA")
                loginProcess.removePlayer(player)
                loginProcess.cancelTasks(player)
            }
        }, 100 * 20L)
        loginProcess.addTask(player, checkTask)
    }
}