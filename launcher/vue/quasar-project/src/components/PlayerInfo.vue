<template>
  <div>
    <div class="container flex">
      <div>
        <div class="avatar-container row">
          <img
            :src="
              'https://minotar.net/helm/' +
              playerStore.data.nickname +
              '/100.png'
            "
            alt=""
            class="avatar"
          />
          <div class="player-text justify-start">
            <p class="player-name">{{ playerStore.data.nickname }}</p>
            <p class="points-text">
              <span style="color: var(--primaryColor)"
                >{{ playerStore.data.score }} pts</span
              >
            </p>
          </div>
        </div>
        <p class="awards-text">
          Suas <span style="color: var(--primaryColor)">conquistas</span>
        </p>
      </div>
      <div class="scroll-shadow"></div>
      <QScrollArea
        style="max-width: 100%"
        dark
        :thumb-style="thumbStyle"
        :bar-style="barStyle"
        :visible="true"
        class="awards-container"
      >
        <div class="awards">
          <div
            class="award pixel-border"
            v-for="award in playerStore.data.awards"
            :key="award.name"
            @mousemove="showPreview(award)"
            @mouseleave="hidePreview"
          >
            <img
              class="award-icon"
              :style="`background: url('awardbg/${award.rarity}.png')`"
              :src="host + '/awards/' + award.id + '/icon'"
            />
            <!-- <img class="award-icon" :src="'awardbg/' + award.rarity + '.png'" /> -->
          </div>
        </div>
      </QScrollArea>
    </div>
    <div class="awards-hover" ref="awardPreview" style="display: none">
      <div class="border-div">
        <div class="awards-upper-info">
          <img
            class="award-icon-large"
            :style="
              selectedAward === null
                ? ''
                : `background: url('awardbg/${selectedAward.rarity}.png')`
            "
            :src="
              selectedAward === null
                ? ''
                : host + '/awards/' + selectedAward.id + '/icon'
            "
          />

          <p>
            {{ selectedAward === null ? "" : selectedAward["name"] }}
          </p>
        </div>
        <p class="award-description">
          {{ selectedAward === null ? "" : selectedAward["description"] ?? "" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { QScrollArea } from "quasar";
import BugText from "./BugText.vue";
import anime from "animejs";
import { ref, onMounted } from "vue";
import axios from "axios";
import { usePlayerStore } from "stores/player";
import { useMouse } from "@vueuse/core";
const playerStore = usePlayerStore();

const { x, y } = useMouse();

var thumbStyle = {
  right: "0.5px",
  borderRadius: "5px",
  backgroundColor: "#ffffff",
  width: "2px",
  opacity: 0.75,
};

var barStyle = {
  right: "0px",
  borderRadius: "9px",
  backgroundColor: "#adadad",
  width: "3px",
  opacity: 1,
};

const host = process.env.SERVER_HOST;

const awardList = ref([]);
const awardPreview = ref(null);
const selectedAward = ref(null);

function showPreview(indexValue) {
  selectedAward.value = indexValue;
  const element = awardPreview.value;
  element.style.display = "block";
  let oX = x.value,
    oY = y.value;
  let {
    x: eX,
    y: eY,
    width: eWidth,
    height: eHeight,
  } = element.getBoundingClientRect();
  oX /= 1.5;
  oY /= 1.5;
  eX /= 1.5;
  eY /= 1.5;
  eWidth /= 1.5;
  eHeight /= 1.5;

  let computedX = oX - eWidth - 10,
    computedY = oY - 10;

  element.style.left = computedX + "px";
  element.style.top = computedY + "px";
}

function hidePreview() {
  const element = awardPreview.value;
  element.style.display = "none";
}

onMounted(() => {
  let n = 0;
  console.log(playerStore.data.nickname);
  let test = playerStore.data.awards.map((i) => {
    return {
      id: n++,
      name: i.name,
      description: i.description,
      type: i.rarity,
      viewable: true,
      color: "martelo_black",
    };
  });
  awardList.value = [];
});
</script>

<style>
.awards-hover {
  position: absolute;
  background: #202020;
  width: 176px;
  height: 96px;
  left: 0;
  top: 0;
  transform-origin: top left;
  z-index: 3;
  padding: 2px;
  border-radius: 4px;
}

.awards-upper-info {
  display: flex;
  align-items: center;
}

.awards-upper-info p {
  margin-bottom: -5px;
  margin-left: 10px;
  font-size: 12px;
}

.awards-hover .border-div {
  border: 2px solid #c0c0c0;
  border-radius: 2px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 6px;
}

.award-icon-large {
  width: 34px;
  height: 34px;
  background-size: cover !important;
}

.award-description {
  margin: 0;
  font-size: 10px;
}

.awards-container {
  margin-top: 10px;
  height: 65px;
  margin-left: 2px;
}

.container {
  margin: 6px;
  padding: 6px;
  background: #202020;
  width: 159px;
  height: 124px;
  flex-direction: column;
  overflow: visible;
  position: relative;
}

.scroll-shadow {
  position: absolute;
  z-index: 1;
  margin-left: -5px;
  width: 100%;
  bottom: 0;
  height: 16px;
  background: rgb(0, 0, 0);
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, #202020 59%);
}

.awards-text {
  margin-bottom: -10px;
  margin-left: 1.5px;
  font-size: 10px;
  position: relative;
}

.awards-text span {
  padding-right: 10px;
}

.awards-text:after {
  content: "";
  position: absolute;
  bottom: 0;
  right: 2px;
  height: 0.65em;
  width: 65px;
  border-top: 0.999px solid rgb(255, 255, 255);
}

.awards {
  /* margin-top: 8px; */
  display: flex;
  flex-wrap: wrap;
  gap: 0px;
  width: auto;
  overflow: visible;
}

.award {
  /* background: #ffbd59; */
  width: 28px;
  height: 28px;

  background-size: cover;
  box-sizing: border-box;
  transition: all 0.1s ease-out;
}

.award-icon {
  width: 25.2px;
  height: 25.2px;
  margin: 1px;
  background-size: contain !important;
  /* --zoom: 25;
  --block-size: 48px;
  border-image: url("assets/achievement-panel.png");
  border-width: calc(var(--block-size) / var(--zoom));
  border-image-width: calc(var(--block-size) / var(--zoom));
  border-image-slice: 43% 43% fill;
  border-image-repeat: stretch; */
}

.award:hover {
  transform: scale(1.05);
}

.points-container {
  margin-bottom: 0px;
}

.avatar-container {
  font-size: 10px;
}

.avatar {
  width: 28px;
  height: 28px;
  margin-left: 1px;
}

.player-text {
  display: flex;
  flex-direction: column;

  margin-left: 4px;
}

.player-text p {
  margin: 0;
  margin-top: -4px;
}

.player-name {
  font-size: 15px;
}

.points-text {
  font-size: 11px;
  margin: 0;
}
</style>
