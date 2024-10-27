<template>
  <div class="server-container">
    <div class="player-count">
      <p>
        <q-icon
          name="wifi"
          style="top: -2px; margin-left: 3px; margin-right: 3px"
        /><span style="color: var(--primaryColor)">{{
          playerStore.server.players
        }}</span>
        {{ playerStore.server.players == 1 ? "player" : "players" }} online!
      </p>
    </div>
    <div class="events-container">
      <p>
        <span style="color: var(--primaryColor)">Eventos</span> acontecendo!!!
      </p>
      <q-carousel
        v-if="playerStore.isLoading == false"
        animated
        v-model="slide"
        infinite
        :autoplay="3000"
        transition-prev="slide-right"
        transition-next="slide-left"
        class="events-carousel"
        @update:model-value="(val) => updateLoading()"
        @before-transition="(nv, ol) => updateLoading()"
      >
        <q-carousel-slide
          v-for="sl in slides"
          :key="sl.id"
          :name="sl.value"
          class="events-slide"
        >
          {{ sl.value }}
        </q-carousel-slide>
      </q-carousel>
      <q-linear-progress
        :value="slides_loader"
        class="slide-loading-bar"
        instant-feedback
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { usePlayerStore } from "stores/player";
import { useVersionStore } from "src/stores/version";
const playerStore = usePlayerStore();
const versionStore = useVersionStore();

const slide = ref(1);

const slides_loader = ref(0.0);

function updateLoading() {
  slides_loader.value = 0;
}

const slides = computed(() => {
  let id = 0;
  return playerStore.server_api_info.events.map((ev) => ({
    id: id++,
    value: ev,
  }));
});

onMounted(() => {
  let limit = 2800;
  let interval = 15;
  let step = interval / limit;
  setInterval(() => {
    if (slides_loader.value < 1) {
      slides_loader.value += step;
    } else {
      slides_loader.value = 1;
    }
  }, interval);
});
</script>

<style>
.server-container {
  width: 160px;
  height: 90px;
  background: #202020;
  border-radius: 2px;
}

.events-carousel,
.events-slide {
  width: 145px;
  height: 30px;
  font-size: 20px;
  background: var(--primaryColor);
  padding: 0;
}

.events-carousel {
  margin-left: 7px;
}

.slide-loading-bar {
  position: absolute;
  width: 145px;
  left: 7px;
  height: 2px;
  bottom: 0;
  background: transparent;
  color: rgba(255, 255, 255, 0.534);
}

.events-slide {
  display: grid;
  align-items: center;
  justify-items: center;
  color: black;
}

.player-count {
  margin: 4px;
  font-size: 15.5px;
}

.player-count p {
  margin-bottom: -5px;
}

.events-container p {
  font-size: 11px;
  margin: 8px;
}

.events-container {
  position: relative;
}
</style>
