import { defineStore } from "pinia";

export const usePlayerStore = defineStore("player", {
  state: () => ({
    data: {
      nickname: "",
      score: 0,
      awards: [],
    },
    server: { online: false, players: 0 },
    server_api_info: { events: [], news: [] },
    isLoading: true,
  }),
});
