package me.lavember.pluginteste

import org.bukkit.entity.Player
import org.bukkit.potion.PotionEffectType
import org.bukkit.scheduler.BukkitTask
import java.util.*
import kotlin.collections.HashSet

class LoginProcess {
    private val inProcess = HashSet<UUID>()
    private val tasksToCancel = HashMap<UUID, MutableList<BukkitTask>>()
    val authy = NormalAuth.instance

    fun contains(e: Player): Boolean {
        return inProcess.contains(e.uniqueId)
    }

    fun addPlayer(p: Player) {
        inProcess.add(p.uniqueId)
    }

    fun removePlayer(p: Player) {
        if(inProcess.contains(p.uniqueId)) {
            p.fallDistance = 0F
            p.removePotionEffect(PotionEffectType.BLINDNESS)
            PreLoginDataStore.restore(p)
            inProcess.remove(p.uniqueId)
        }
    }

    fun addTask(p: Player, task: BukkitTask) {
        if(!tasksToCancel.containsKey(p.uniqueId)) {
            tasksToCancel[p.uniqueId] = mutableListOf()
        }
        tasksToCancel[p.uniqueId]?.add(task)
    }

    fun cancelTasks(p: Player) {
        if(tasksToCancel.containsKey(p.uniqueId)) {
            tasksToCancel[p.uniqueId]?.forEach { it.cancel() }
            tasksToCancel.remove(p.uniqueId)
        }
    }
}