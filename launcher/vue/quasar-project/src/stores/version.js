import { defineStore } from "pinia";

export const useVersionStore = defineStore("version", {
  state: () => ({
    data: {
      isUpdating: false,
      shouldUpdateLauncher: false,
      bell: false,
    },
  }),
});
