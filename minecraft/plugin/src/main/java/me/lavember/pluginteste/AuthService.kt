package me.lavember.pluginteste

import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import kotlinx.coroutines.runBlocking
import org.bukkit.entity.Player

class AuthService {
    private val client = HttpClient(CIO) {
    }
    private val route = "http://149.28.101.35:5000/code/verify?code="
    private val gson = Gson()
    private val mapType = object : TypeToken<Map<String, Any>>() {}.type

    fun verify(code: String, player: Player): Boolean {
        return runBlocking {
            val response: HttpResponse = client.get(route + code)
            val parsedBody: Map<String, Any> = gson.fromJson(response.bodyAsText(), mapType)
            val valid = parsedBody["valid"] as Boolean
            val playerName = parsedBody["player_name"] as String?

            valid && player.name == playerName
        }

    }
}