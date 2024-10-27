<template>
  <div class="launcher">
    <div class="jornal">
      <JournalContainer />
    </div>
    <div class="bottom-row">
      <div class="side-square player-square">
        <PlayerInfo />
      </div>

      <div class="side-square server-square">
        <ServerInfo />
      </div>

      <div class="play-container">
        <q-linear-progress
          rounded
          size="13px"
          :value="progress_val"
          class="progress-bar"
        >
          <div class="absolute-full flex flex-center">
            <q-badge
              style="background-color: var(--primaryColor)"
              text-color="black"
              :label="Math.min(Math.floor(progress_val * 100), 100) + '%'"
            />
          </div>
        </q-linear-progress>
      </div>
      <q-btn
        push
        :label="playando_text"
        @click="playAction"
        :class="
          'play-button ' + (versionStore.data.bell ? 'play-button-bell' : '')
        "
        :ripple="false"
        :loading="loading"
        :disable="play_disabled || versionStore.data.isUpdating === true"
      >
        <template v-slot:loading>
          {{ playando_text }}
        </template>
      </q-btn>
      <div class="footer">
        <p>
          <a href="#">suporte</a> / <a href="#">bug report</a> /
          <a href="#">sla tlg</a> <br />
          v. launcher 0.001
        </p>
        <q-btn
          icon="settings"
          class="settings-btn"
          :ripple="false"
          :enabled="versionst"
          flat
          round
          size="12px"
          padding="none"
          @click="settings_show = true"
        />
      </div>
    </div>
    <q-dialog
      v-model="settings_show"
      position="top"
      :backdrop-filter="'blur(2.5px)'"
    >
      <SettingsDialog></SettingsDialog>
    </q-dialog>
  </div>
</template>

<script setup>
import { onBeforeMount, onMounted, ref } from "vue";
import PlayerInfo from "components/PlayerInfo.vue";
import JournalContainer from "../components/JournalContainer.vue";
import ServerInfo from "../components/ServerInfo.vue";
import SettingsDialog from "../components/SettingsDialog.vue";
import axios from "axios";
import { usePlayerStore } from "stores/player";
import { useConfigStore } from "src/stores/config";
import { useVersionStore } from "src/stores/version";
import { setCssVar } from "quasar";
const playerStore = usePlayerStore();
const versionStore = useVersionStore();
const configStore = useConfigStore();

const loading = ref(false);
const play_disabled = ref(false);
const progress_val = ref(0.0);
const playando_text = ref(versionStore.data.bell ? "OI LINDA" : "PLAY");
const playando_interval = ref(null);
const settings_show = ref(false);

const update_playando_text = () => {
  playando_text.value = versionStore.data.bell ? "OI LINDA" : "PLAY";
};

const play_callback = (type) => {
  switch (type) {
    case "open":
      clearInterval(playando_interval.value);
      loading.value = false;
      playando_text.value = "PLAYADO!";
      play_disabled.value = true;
      progress_val.value = 0.0;

      if (shouldHideLauncher()) {
        window.myWindowAPI.hide();
      }

      break;
    case "close":
      update_playando_text();
      play_disabled.value = false;
      break;
    default:
      break;
  }
};
if (window.eel !== undefined) {
  window.eel.expose(play_callback, "play_callback");
  window.eel.expose(window.myWindowAPI.show, "show_hook");
}

function shouldHideLauncher() {
  let shouldHideLauncher = configStore.data["closeLauncher"];
  return shouldHideLauncher == null ? true : shouldHideLauncher == "1";
}

const playAction = async () => {
  console.log("play play!");

  loading.value = true;
  playando_text.value = versionStore.data.bell ? "LINDA" : "PLAYANDO";
  playando_interval.value = setInterval(() => {
    playando_text.value =
      playando_text.value + (versionStore.data.bell ? "!" : ".");

    if (versionStore.data.bell) {
      if (playando_text.value == "LINDA!!!!") {
        playando_text.value = "LINDA";
      }
    } else {
      if (playando_text.value == "PLAYANDO....") {
        playando_text.value = "PLAYANDO";
      }
    }

    if (progress_val.value < 1) {
      progress_val.value += 0.05;
    }
  }, 300);
  console.log(playerStore.data.nickname);
  let memoryAllocation = configStore.data["ram"];

  memoryAllocation = memoryAllocation == null ? 3 : memoryAllocation;
  let playerCode = await getPlayCode();

  eel.start_mine(
    playerStore.data.nickname,
    "play_callback",
    memoryAllocation,
    shouldHideLauncher(),
    playerCode
  );
};

defineOptions({
  name: "IndexPage",
  inheritAttrs: false,
  customOptions: {},
});

let host = process.env.SERVER_HOST;
async function loadPlayerData() {
  let res = await axios.get(host + "/players/@me", {
    headers: {
      Authorization: configStore.getToken(),
    },
  });
  playerStore.data = res.data;
  versionStore.data.bell = playerStore.data.nickname == "Bell_54";
  update_playando_text();
  setCssVar("primary", versionStore.data.bell ? "#ffc6d9" : "#ffbd59");
}

async function loadServerData() {
  let res = await axios.get("https://api.mcsrvstat.us/3/23.230.3.162:25698");
  if (res.status == 200 && res.data !== undefined) {
    playerStore.server = {
      online: res.data.online,
      players: res.data.online ? res.data.players.online : 0,
    };
  }
}

async function loadServerInfo() {
  let res = await axios.get(host + "/server/info", {
    headers: {
      Authorization: configStore.getToken(),
    },
  });

  console.log(res);
  if (res.status !== 200) return;

  playerStore.server_api_info = res.data;
}

async function getPlayCode() {
  let res = await axios.get(host + "/code/generate", {
    headers: {
      Authorization: configStore.getToken(),
    },
  });
  return res.data.code;
}

onMounted(async () => {
  if (process.env.NODE_ENV !== "development") {
    await loadPlayerData();
    await loadServerData();
    await loadServerInfo();
  }

  playerStore.isLoading = false;
});
</script>

<style>
.settings-btn {
  background: transparent;
  color: white;
  height: 12px;
}

a {
  color: #38b6ff;
  text-decoration-line: underline;
  text-decoration-thickness: 1px;
}

.footer {
  font-size: 8px;
  color: #c0c0c0;
  display: flex;
  justify-content: space-between;
}

.player-square {
  height: 135px;
}

.launcher {
  width: 642px;
  height: 400px;
  background: #202020;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  flex-direction: column;
  padding: 10px;
  padding-top: 2px;
  position: absolute;
}

.progress-bar {
  width: 164px;
  border-radius: 2px;
}

.play-button {
  width: 170px;
  height: 51px;
  background: var(--primaryColor);
  color: black;
  font-size: 19px;
  font-weight: 500;
  font-family: "Mine";

  border-bottom: var(--borderColor) 5px solid;
  border-right: var(--borderColor) 5px solid;
  border-radius: 2px;
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), border 0.3s linear !important;
}

.play-button.play-button-bell:hover {
  animation: wobble-hor-bottom 0.8s both;
}

@keyframes wobble-hor-bottom {
  0%,
  100% {
    -webkit-transform: translateX(0%);
    transform: translateX(0%);
    -webkit-transform-origin: 50% 50%;
    transform-origin: 50% 50%;
  }

  15% {
    -webkit-transform: translateX(-10px) rotate(-2deg);
    transform: translateX(-10px) rotate(-2deg);
  }

  30% {
    -webkit-transform: translateX(5px) rotate(2deg);
    transform: translateX(5px) rotate(2deg);
  }

  45% {
    -webkit-transform: translateX(-5px) rotate(-1.2deg);
    transform: translateX(-5px) rotate(-1.2deg);
  }

  60% {
    -webkit-transform: translateX(3px) rotate(0.8deg);
    transform: translateX(3px) rotate(0.8deg);
  }

  75% {
    -webkit-transform: translateX(-2px) rotate(-0.6deg);
    transform: translateX(-2px) rotate(-0.6deg);
  }
}

.play-button:hover {
  /* border-bottom: #c48323 5px solid;
  border-right: #c48323 5px solid; */
  border-radius: 2px;
}

.play-button::before {
  border-bottom: none;
  box-shadow: none;
}

/* .play-button:active {
  background: #ffbd59;
} */

.jornal {
  width: 433px;
  height: 374px;
  background: #545454;
}

.bottom-row {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-wrap: wrap;
}

.play-container {
  width: 170px;
  height: 22px;
  background: #545454;
  display: grid;
  align-items: center;
  justify-items: center;
  border-radius: 2px;
}

.side-square {
  width: 170px;

  background: #545454;
  display: grid;
  align-items: center;
  justify-items: center;
  border-radius: 2px;
}

.server-square {
  height: 102px;
}
</style>
