package me.lavember.pluginteste

import net.md_5.bungee.api.ChatMessageType
import net.md_5.bungee.api.chat.TextComponent
import org.bukkit.Color
import org.bukkit.FireworkEffect
import org.bukkit.Location
import org.bukkit.Sound
import org.bukkit.command.Command
import org.bukkit.command.CommandExecutor
import org.bukkit.command.CommandSender
import org.bukkit.entity.Firework
import org.bukkit.entity.Player

class LoginCommand : CommandExecutor {
    private val loginProcess = NormalAuth.loginProcess
    private val authy = NormalAuth.instance
    private val authService = NormalAuth.authService

    override fun onCommand(sender: CommandSender, command: Command, label: String, args: Array<String>): Boolean {
        if(sender is Player){
            val p: Player = sender
            if(args.size != 1){
                return false
            }

            val token = args[0]

            if(authService.verify(token, p)){
                login(p)
            } else {
                p.sendMessage("nao sei voce mas tem um burro entre nos ... (senha errada, faça um bug-report! )")
                return true
            }
        }
        return false
    }

    private fun login(p: Player){
        loginProcess.removePlayer(p)
        p.spigot().sendMessage(ChatMessageType.ACTION_BAR, TextComponent("Bem vindo!"));
        // runFireWorks(p, Color.fromRGB(255, 255 ,255))
        p.playSound(p.location, Sound.ENTITY_EXPERIENCE_ORB_PICKUP, 1F, 1F)
        authy.server.scheduler.runTaskLater(authy, Runnable {
            p.playSound(p.location, Sound.ENTITY_EXPERIENCE_ORB_PICKUP, 1F, 1F)
            p.playSound(p.location, Sound.ENTITY_EXPERIENCE_BOTTLE_THROW, 1F, 1F)
        }, 5L)
        authy.server.scheduler.runTaskLater(authy, Runnable {
            p.playSound(p.location, Sound.ENTITY_EXPERIENCE_ORB_PICKUP, 1F, 1F)
            p.playSound(p.location, Sound.ENTITY_EXPERIENCE_BOTTLE_THROW, 1F, 1F)
        }, 10L)
    }

    private fun runFireWorks(p : Player, c : Color) {
        authy.server.scheduler.runTaskLater(authy, Runnable {
            val loc = Location(p.world, p.location.x, p.location.y - 1, p.location.z)
            val firework = p.world.spawn(loc, Firework::class.java)
            val fireworkMeta = firework.fireworkMeta
            fireworkMeta.addEffect(
                FireworkEffect.builder()
                .flicker(true)
                .trail(true)
                .with(FireworkEffect.Type.STAR)
                .with(FireworkEffect.Type.BALL)
                .with(FireworkEffect.Type.BALL_LARGE)
                .withColor(Color.GRAY)
                .withColor(c)
                .withColor(Color.WHITE)
                .build()
            )

            fireworkMeta.power = 0
            firework.fireworkMeta = fireworkMeta
        }, 5L)
    }

}