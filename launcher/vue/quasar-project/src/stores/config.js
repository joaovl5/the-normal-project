import { defineStore } from "pinia";

export const useConfigStore = defineStore("config", {
  state: () => ({
    data: {},
  }),
  actions: {
    loadConfig() {
      return new Promise((resolve, reject) => {
        if (window.eel === undefined) resolve();

        window.eel.config_dump()((res) => {
          this.data = res;

          resolve();
        });
      });
    },
    updateConfig() {
      if (window.eel === undefined) return;

      for (let k in this.data) {
        let v = this.data[k];
        window.eel.config_set(k, v);
      }
    },
    async checkAuthenticated() {
      let token = this.data["access_token"];

      if (token === undefined) {
        await this.loadConfig();
        return this.checkAuthenticated();
      }

      return token !== "";
    },
    getToken() {
      return this.data["access_token"];
    },
    setToken(value) {
      this.data["access_token"] = value;
      this.updateConfig();
    },
  },
});
