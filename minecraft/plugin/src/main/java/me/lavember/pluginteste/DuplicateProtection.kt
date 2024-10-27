package me.lavember.pluginteste

import org.bukkit.entity.Player
import org.bukkit.event.player.PlayerLoginEvent

object DuplicateProtection {
    val plugin = NormalAuth.instance

    fun check(e: PlayerLoginEvent) {
        val p = e.player
        if(plugin.server.getPlayer(p.name) != null) {
            e.disallow(PlayerLoginEvent.Result.KICK_OTHER, "PODE IR SAINDO! Esse jogador já está logado!")
        }
        val duplicates = getIpDuplicates(p)
        if(duplicates.size > 5) {
            e.disallow(PlayerLoginEvent.Result.KICK_OTHER, "PODE IR SAINDO! Voce ja ta com mtos jogadores no mesmo ip!")
        }
    }

    fun getIpDuplicates(p: Player): HashSet<String> {
        val duplicates = HashSet<String>()
        duplicates.add(p.name)
        val ip = p.address?.address?.hostAddress
        return plugin.server.onlinePlayers.filter{it.address?.address?.hostAddress == ip}.mapTo(duplicates) {it.name}
    }
}