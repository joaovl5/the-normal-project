<template>
  <q-card class="cfg-dialog" :style="`--primaryColor: ${versionStore.data.bell ? '#ffc6d9' : '#ffbd59'
    }; --borderColor: ${versionStore.data.bell ? '#e592ae' : '#f1a22a'}`">
    <div class="cfg-container">
      <div>
        <p class="cfg-title">Conta</p>
        <p class="cfg-text">
          Tipo de conta:
          <span style="color: var(--primaryColor); margin-right: 5px">Discord</span>
          <button class="cfg-btn" @click="logout">deslogar</button>
        </p>

        <!-- <button class="cfg-btn">trocar conta</button> -->
      </div>
      <div class="flex justify-between cfg-divided">
        <div>
          <p class="cfg-title">Jogo</p>
          <div class="cfg-prop">
            <p id="title">Memória Alocada</p>
            <p id="description">É recomendável usar acima de 3Gb</p>
            <div class="cfg-slider-container">
              <q-slider v-model="modelMemoria" :step="1" :min="1" :max="8" thumb-size="15px" class="cfg-slider" dark
                markers marker-labels-class="cfg-slider-labels" :marker-labels="[1, 2, 3, 4, 5, 6, 7, 8].map((i) => ({
                  value: i,
                  label: i + 'G',
                }))
                  " label :label-value="modelMemoria + 'Gb'" />
            </div>
          </div>
        </div>
        <div>
          <p class="cfg-title">Launcher</p>
          <div class="cfg-prop">
            <q-checkbox v-model="modelLauncherClose" size="25px" dense dark color="primary"
              label="Fechar launcher ao abrir jogo" />
          </div>
        </div>
      </div>
    </div>
  </q-card>
</template>

<script setup>
import { useRouter } from "vue-router";
import { onMounted, onUnmounted, ref } from "vue";
import { useConfigStore } from "src/stores/config";
import { useVersionStore } from "src/stores/version";
const router = useRouter();
const configStore = useConfigStore();
const versionStore = useVersionStore();

const modelMemoria = ref(1);
const modelLauncherClose = ref(false);

function logout() {
  configStore.setToken("");
  router.push("/login");
}

function get(key) {
  return configStore.data[key];
}

function set(key, value) {
  configStore.data[key] = value;
}

function loadSettings() {
  let cfgMemoria = get("ram");
  if (cfgMemoria !== null) {
    modelMemoria.value = parseInt(cfgMemoria);
  }

  let cfgLauncherClose = get("closeLauncher");
  if (!cfgLauncherClose !== null) {
    modelLauncherClose.value = cfgLauncherClose == "1";
  }
}

function updateSettings() {
  set("ram", modelMemoria.value.toString());
  set("closeLauncher", modelLauncherClose.value == true ? "1" : "0");
  configStore.updateConfig();
}

onMounted(() => {
  loadSettings();
});

onUnmounted(() => {
  updateSettings();
});
</script>

<style lang="css">
.cfg-divided {
  gap: 10px;
}

.cfg-slider-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.cfg-slider {
  width: 92%;
}

.cfg-prop.slider {
  display: flex;
}

.cfg-slider-labels {
  margin-top: -8px;
  font-size: 9px;
}

.cfg-btn {
  border: 1px solid var(--primaryColor);
  border-radius: 4px;
  color: white;
  background: transparent;
  height: 18px;
  transition: all 0.2s ease;
  font-size: 11px;
  cursor: pointer;
  padding: 0 2px;
}

.cfg-prop p {
  margin: 0;
}

.cfg-prop #title {
  font-size: 12px;
}

.cfg-prop #description {
  font-size: 9px;
  color: #c0c0c0;
}

.cfg-btn:hover {
  background: #333333;
}

.cfg-btn:active {
  background: #4a4a4a;
  transform: translateY(5%) scale(95%);
}

.cfg-dialog {
  background: #202020;
  border: 2px solid var(--primaryColor);
  border-top: none;
  border-radius: 2px;
  min-width: 335px;
  font-size: 10px;
  padding: 10px;
}

p.cfg-text {
  margin-bottom: 0;
  font-size: 12px;
}

.cfg-title {
  font-family: "Mine";
  font-size: 14px;
  margin: 0;
}

.cfg-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>
