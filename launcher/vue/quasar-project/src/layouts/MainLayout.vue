<template>
  <div :style="`--primaryColor: ${versionStore.data.bell ? '#ffc6d9' : '#ffbd59'
    }; --borderColor: ${versionStore.data.bell ? '#e592ae' : '#f1a22a'}`">
    <div class="menubar">
      <q-bar dense class="bar q-electron-drag">
        <div class="col text-center menutitle" style="color: #ffc6d9" v-if="versionStore.data.bell">
          <b>oiiiiiii linda linda bellbs launcher!!!</b>
        </div>
        <div class="col text-center menutitle" v-else>isso é um launcher?</div>

        <q-space />
        <q-btn v-if="versionStore.data.bell" dense flat round class="menubtn closeBell" icon="heart_broken" size="7px"
          style="color: #ffc6d9" @click="closeApp" />
        <q-btn v-else dense flat round class="menubtn" icon="lens" size="5.5px" color="red" @click="closeApp" />
        <q-btn v-if="versionStore.data.bell" dense flat round class="menubtn minimizeBell" icon="favorite_border"
          size="7px" style="color: #ffc6d9" @click="minimize" />
        <q-btn v-else dense flat round class="menubtn" icon="lens" size="5.5px" color="yellow" @click="minimize" />
      </q-bar>
    </div>
    <div style="
        z-index: 2;
        position: absolute;
        width: 642px;
        height: 400px;
        background-color: black;
      " ref="loaddiv" @loadstart="loaddiv.style.opacity = 0.5" v-if="playerStore.isLoading"
      class="flex justify-center items-center">
      <div class="loading-item">
        <p>carregando...</p>
      </div>
    </div>
    <div class="transition-container">
      <router-view v-slot="{ Component }">
        <transition name="slide">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useVersionStore } from "src/stores/version";
import { usePlayerStore } from "src/stores/player";
import { setCssVar } from "quasar";

export default defineComponent({
  name: "MainLayout",

  components: {},
  setup() {
    function minimize() {
      window.myWindowAPI.minimize();
    }

    function toggleMaximize() {
      window.myWindowAPI.toggleMaximize();
    }

    function closeApp() {
      window.eel.trigger_quit();
      window.myWindowAPI.close();
    }

    const playerStore = usePlayerStore();
    const versionStore = useVersionStore();
    const loaddiv = ref(null);

    // setCssVar("primary", versionStore.data.bell ? "#ffc6d9" : "#ffbd59");

    return {
      versionStore,
      minimize,
      toggleMaximize,
      closeApp,
      playerStore,
      loaddiv,
    };
  },
});
</script>
<style>
.loading-item {
  animation: loadingAnim forwards 1s infinite;
}

.loading-item p {
  animation: scalingAnim forwards 60s;
}

@keyframes loadingAnim {
  0% {
    transform: rotateY(0deg) scale(1);
  }

  50% {
    transform: rotateY(180deg) scale(1);
    color: #ffbd59;
  }

  100% {
    transform: rotateY(360deg) scale(1);
  }
}

@keyframes scalingAnim {
  0% {
    transform: scale(1);
  }

  100% {
    transform: scale(20);
  }
}

.closeBell:hover {
  animation: closeBellAnim forwards 1s infinite ease-out;
}

.minimizeBell:hover {
  animation: minimizeBellAnim forwards 1.2s infinite ease-out;
}

@keyframes closeBellAnim {
  0% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(15deg);
  }

  75% {
    transform: rotate(-15deg);
  }

  0% {
    transform: rotate(0deg);
  }
}

@keyframes minimizeBellAnim {
  0% {
    transform: rotateX(0);
  }

  20% {
    transform: rotateX(90deg);
  }

  60% {
    transform: rotateX(90deg);
  }

  100% {
    transform: rotateX(0);
  }
}

.menubar .bar {
  height: 15px;
  background: #202020;
}

.menutitle {
  font-size: 11px;
  position: absolute;
  left: 0;
  right: 0;
  margin-left: auto;
  margin-right: auto;
}

.menubtn {
  padding: 0;
  margin: 0;
}

.transition-container {
  position: relative;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
}

.slide-enter-to {
  position: absolute;
  transform: translateX(0);
}

.slide-enter-from {
  position: absolute;
  transform: translateX(642px);
}

.slide-leave-to {
  position: absolute;
  transform: translateX(-642px);
}

.slide-leave-from {
  position: absolute;
  transform: translateX(0);
}
</style>
