<template>
  <div class="login-page">
    <div>
      <p class="login-header"><img src="logo.png" />ISSO É NORMAL?</p>
      <div class="login-card">
        <div class="login-outline"></div>
        <div class="login-fill"></div>
        <div class="login-content flex justify-center items-center">
          <transition name="slide">
            <div
              v-if="show_cadastro"
              class="flex justify-center items-center cadastro-card"
            >
              <div class="flex justify-center">
                <p class="login-title">cadastre-se!</p>
                <p class="login-subtitle">Escolha seu nickname no servidor!</p>
              </div>
              <div class="flex justify-center login-btn-container">
                <q-input
                  outlined
                  dense
                  dark
                  label="nickname"
                  color="primary"
                  label-color="white"
                  input-class="login-input"
                  class="login-qinput"
                  v-model="cadastro_name"
                >
                  <template v-slot:after>
                    <q-btn
                      round
                      square
                      flat
                      color="white"
                      icon="verified"
                      class="login-check-btn"
                      size="12px"
                      @click="handle_register_name"
                    />
                  </template>
                </q-input>
                <p class="login-subsubtitle">
                  <span style="color: #ff7777"><b>Cuidado:</b></span> essa
                  escolha é
                  <u
                    style="
                      text-decoration: none;
                      border-bottom: 1px dotted white;
                    "
                    >irreversível </u
                  >.
                  <q-tooltip
                    anchor="top start"
                    self="top start"
                    :offset="[-210, 100]"
                    class="login-tooltip"
                    max-width="200px"
                  >
                    Atualmente é impossível alterar o nick de uma conta já
                    criada, por limitações do servidor e possíveis conflitos com
                    plugins.
                  </q-tooltip>
                </p>
              </div>
            </div>
            <div v-else class="flex justify-center items-center inner-content">
              <p class="login-title">FAÇA LOGIN!</p>
              <button class="discord-btn" @click="request_auth_url">
                CONECTE-SE!
              </button>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import axios from "axios";
import { usePlayerStore } from "src/stores/player";
import { useConfigStore } from "src/stores/config";

const router = useRouter();
const show_cadastro = ref(false);
const cadastro_name = ref("");

const configStore = useConfigStore();

function handle_login(token, is_new_player) {
  window.eel.bring_window_to_front();
  configStore.setToken(token);
  if (is_new_player) {
    show_cadastro.value = true;
  } else {
    complete_login();
  }
}
let host = process.env.SERVER_HOST;
function handle_register_name() {
  axios
    .get(host + "/players/@me/register?nickname=" + cadastro_name.value, {
      headers: {
        Authorization: configStore.getToken(),
      },
    })
    .then((res) => {
      if (res.status == 200) {
        playerStore.isLoading = true;
        complete_login();
      }
    });
}

function complete_login() {
  router.push("/");
}

async function request_auth_url() {
  let res = (await axios.get(host + "/auth/discord/url")).data;
  if (typeof res.url !== undefined) {
    window.eel.open_url(res.url);
  } else {
  }
}

if ("eel" in window) {
  window.eel.expose(handle_login, "handle_login");
}

const playerStore = usePlayerStore();

onMounted(() => {
  playerStore.isLoading = false;
});
</script>
<style>
.login-tooltip {
  background: #202020;
  border: 1px dashed rgba(255, 255, 255, 0.342);
}

.login-btn-container {
  gap: 4px;
}

.login-check-btn {
  border: 1px solid rgba(255, 255, 255, 0.548);
  border-radius: 6px;
}

.login-subsubtitle {
  font-size: 11px;
  text-align: center;
  font-family: "Retropix";
}

.login-qinput {
  font-family: "Retropix";
}

.login-input {
  font-family: "Retropix";
}

.cadastro-card {
  padding: 16px;
  gap: 10px;
}

.login-subtitle {
  font-family: "Retropix";
  text-align: center;
  font-size: 13px;
}

.login-card:hover .login-outline {
  transform: scale(1.01) translate(-5px, 0px);
}

.login-card:hover .login-fill {
  transform: scale(0.95) translate(7px, 10px);
}

.login-card:hover .login-content {
  transform: scale(1.02);
}

.login-header {
  font-size: 20px;
  margin-top: 22px !important;
  align-self: flex-start;
}

.login-header img {
  margin-bottom: -15px;
  margin-right: 20px;
  width: 50px;
  height: 50px;
  border: 2px solid #f3b14d;
  border-radius: 3px;
}

.login-page {
  width: 642px;
  height: 400px;
  background-image: url("/wallpaper.jpg");
  background-size: cover;
  position: absolute;
  font-family: "Mine";
  font-size: 12px;
}

.inner-content {
  gap: 16px;
}

.login-page p {
  margin: 0;
}

.discord-btn {
  width: 204px;
  height: 41px;
  background: #5662f6;
  color: white;
  border: none;
  border-radius: 6px;
  transition: all 0.3s ease-in-out;
  cursor: pointer;
}

.discord-btn:hover {
  transform: scale(1.05);
  background: #4149bb;
}

.discord-btn:active {
  transform: scale(1);
  background: #727bff;
}

.discord-btn img {
  width: 26px;
  height: 26px;
}

.login-title {
  color: #f3b04d;
  font-size: 22px;
}

.login-page > div {
  width: 100%;
  height: 100%;
  background: #000000c3;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  position: absolute;
  bottom: 25%;
  left: 30%;
}

.login-fill {
  position: absolute;
  z-index: -1;
  bottom: -5px;
  left: 5px;
  width: 264px;
  height: 207px;
  background: #f3b04d;
  border: 1px solid #f3b04d;
  border-radius: 3px;
  z-index: 2;
  transition: all 0.75s ease;
}

.login-content {
  position: absolute;
  overflow: hidden;
  transition: all 1s ease-in-out;
  z-index: 2;
  bottom: 0;
  width: 264px;
  height: 207px;
  background: #202020;
  border: 2px solid #f3b04d;
  border-radius: 3px;
  z-index: 2;
}

.login-outline {
  transition: all 0.75s ease;
  position: absolute;
  bottom: 10px;
  left: -10px;
  width: 264px;
  height: 207px;
  background: transparent;
  border: 1px solid #f3b04d;
  border-radius: 3px;
}
</style>
