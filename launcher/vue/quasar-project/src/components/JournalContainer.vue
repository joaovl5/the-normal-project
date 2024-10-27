<template>
  <div class="journal-container">
    <div class="header flex justify-between">
      <div class="header-left">
        <div
          :class="versionStore.data.bell ? 'logo bellLogo' : 'logo'"
          :style="`background-image: url('/${
            versionStore.data.bell ? 'bellbs' : 'logo'
          }.png'); --borderColor: ${
            versionStore.data.bell ? '255, 198, 217' : '255, 189, 89'
          }`"
        ></div>
        <p class="title headerBell" v-if="versionStore.data.bell">
          BELLBS LINDA!!!
        </p>
        <p class="title" v-else>ISSO É NORMAL?</p>
      </div>
      <div class="header-btns">
        <q-btn
          push
          icon="img:cord.png"
          :ripple="false"
          class="header-btn icon-btn"
          @click="openDiscord"
        />
        <q-btn push class="header-btn" :ripple="false" disabled
          >Patch Notes</q-btn
        >
        <q-btn
          push
          disabled
          icon="img:dario.png"
          :ripple="false"
          class="header-btn icon-btn"
        />
      </div>
    </div>
    <div class="slide-container" v-if="playerStore.isLoading == false">
      <swiper-container
        :effect="'cards'"
        :grabCursor="true"
        :modules="modules"
        :mousewheel="true"
        :cardsEffect="{ slideShadows: true, rotate: false, perSlideOffset: 43 }"
        :slideActiveClass="'active-slide'"
        class="carousel"
      >
        <swiper-slide class="swiper-slide" v-for="slide in news" :key="slide.id"
          ><div class="slide">
            <img
              :src="host + slide.value"
              class="slide-img"
              :style="
                versionStore.data.bell
                  ? 'filter: hue-rotate(289deg) saturate(0.5);'
                  : ''
              "
            /></div
        ></swiper-slide>
      </swiper-container>

      <!-- <q-carousel
      animated
      v-model="slide"
      arrows
      infinite
      transition-prev="slide-right"
      transition-next="slide-right"
      class="carousel"
    >
      <q-carousel-slide :name="1" img-src="jornal.png" class="slide" />
      <q-carousel-slide :name="2" img-src="jornal.png" class="slide" />
      <q-carousel-slide :name="3" img-src="jornal.png" class="slide" />
    </q-carousel> -->
    </div>
  </div>
</template>
<script setup>
import { computed, ref } from "vue";

import Swiper from "swiper";
import "swiper/css";
import "swiper/css/bundle";

const versionStore = useVersionStore();
const playerStore = usePlayerStore();

let host = process.env.SERVER_HOST;

const news = computed(() => {
  let i = 0;
  console.log(playerStore.server_api_info.news);
  return playerStore.server_api_info.news.map((v) => ({ id: i++, value: v }));
});

// Now you can use Swiper
import { EffectCards, Mousewheel, Navigation } from "swiper/modules";
import { useVersionStore } from "src/stores/version";
import { usePlayerStore } from "src/stores/player";
const modules = [EffectCards, Mousewheel, Navigation];

function openDiscord() {
  window.eel.open_url("https://discord.gg/tbSq3WuQxw");
}
</script>
<style>
.logo {
  width: 30px;
  height: 30px;
  margin: 0;
  margin-left: 4px;
  border: 2px solid;
  border-color: rgb(var(--borderColor));
  border-radius: 2px;
  transition: all 0.5s ease;
  transform: rotate(0deg);
  background-size: cover;
  position: relative;
  overflow: hidden;
}

.logo:hover {
  animation: rotateAnim forwards 1s infinite;
  animation-timing-function: ease-in-out;
  box-shadow: 0 0 6px rgb(var(--borderColor));
}

.logo:before {
  content: " ";
  position: absolute;
  top: 0;
  left: -50px;
  width: 50px;
  height: 50px;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(var(--borderColor), 0.3),
    transparent
  );
  animation: shineAnim forwards 2s infinite;
  transition: all 650ms;
}

.logo.bellLogo:hover {
  animation: rotateAnimBell forwards 1s infinite;
}

.headerBell {
  font-weight: bolder;
  animation: shineHeaderAnim forwards 5s infinite;
}

@keyframes shineHeaderAnim {
  0% {
    text-shadow: 0 0 0px rgba(255, 198, 217, 0.5);
  }
  50% {
    text-shadow: 0 0 10px rgba(255, 198, 217, 0.7);
  }
  100% {
    text-shadow: 0 0 0px rgba(255, 198, 217, 0.5);
  }
}

@keyframes shineAnim {
  0% {
    left: -50px;
  }
  20% {
    left: 100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes rotateAnim {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes rotateAnimBell {
  0% {
    transform: rotate3d(0);
  }
  100% {
    transform: rotate3d(1, 1, 1, 360deg);
  }
}

.header-left {
  display: flex;
  flex-direction: row;
}

.title {
  font-size: 16px;
  margin-left: 10px;
  margin-top: 4px;
}

.journal-container {
  font-family: "Mine";
}

.active-slide img {
  opacity: 1 !important;
}

.header-btn {
  background: #f6ffff;
  color: #636363;
  padding: 6px;
  font-size: 8.5px;
  padding: 6px;
  margin-left: 5px;
  border-radius: 2px;
  height: 30px;
}

.header-btn.icon-btn {
  font-size: 12px;
  padding: 0px;
  height: 30px;
  width: 30px;
}

.navNext {
  background: black;
}

.header {
  height: 49px;
  margin: 0px 15px 0 15px;
  padding-top: 15px;
}

.carousel {
  width: 285px !important;
  height: 317px !important;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-items: center;
  background: none;
  margin-left: 20px;
}

.swiper-slide {
  box-shadow: 37px 13px 30px -10px rgba(0, 0, 0, 0.74);
  -webkit-box-shadow: 37px 13px 30px -10px rgba(0, 0, 0, 0.74);
  -moz-box-shadow: 37px 13px 30px -10px rgba(0, 0, 0, 0.74);
}

.slide {
  background: #545454;
  width: 285px;
  height: 317px;
  /* transform-origin: top left;
  transform: scale(0.5); */
  margin: 10px;
  margin: 0;
}

.slide img {
  opacity: 0.5;
  transition: opacity 0.2s ease 0s;
}

.slide-container {
  width: 434px;
  height: 325px;
  display: flex;
  align-items: center;
  justify-items: start;
  overflow: hidden;
}

.slide-img {
  width: auto;
  height: 317px;
  image-rendering: -webkit-optimize-contrast;
  /* image-rendering: pixelated; */
}
</style>
