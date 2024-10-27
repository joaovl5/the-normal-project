<template>
  <router-view />
</template>

<script>
import { defineComponent } from "vue";
import axios from "axios";
import { useVersionStore } from "./stores/version";
import { useRouter } from "vue-router";
import { useConfigStore } from "./stores/config";
import "vue3-toastify/dist/index.css";
import { toast } from "vue3-toastify";

export default defineComponent({
  name: "App",
  data: () => ({
    versionStore: useVersionStore(),
    configStore: useConfigStore(),
    router: useRouter(),
  }),
  methods: {
    log(msg) {
      eel.plog(msg);
      console.log(msg);
    },
    downloadVersion(latest_version) {
      let versionStore = this.versionStore;
      let configStore = this.configStore;

      const notification = toast.loading(
        "Atualizando modpack! Por favor, aguarde...",
        {
          theme: "dark",
          type: "default",
          position: toast.POSITION.BOTTOM_RIGHT,
        }
      );

      function downloadCallback(r) {
        versionStore.data.isUpdating = false;
        if (r === true) {
          toast.update(notification, {
            render: "Atualização baixada com sucesso!",
            autoClose: true,
            closeOnClick: true,
            closeButton: true,
            isLoading: false,
          });
          configStore.data["installed_version"] = latest_version;
          configStore.updateConfig();
        } else {
          toast.update(notification, {
            render:
              "Erro ao atualizar! Tente novamente. Caso persistir, faça um bug report.",
            autoClose: true,
            closeOnClick: true,
            closeButton: true,
            isLoading: false,
          });
        }
      }
      window.eel.expose(downloadCallback, "downloadCallback");

      versionStore.data.isUpdating = true;

      return new Promise((resolve, reject) => {
        window.eel.download_version(latest_version, "downloadCallback");
        resolve();
      });
    },
    async checkVersion() {
      let host = process.env.SERVER_HOST;
      let back_data = await axios.get(host + "/version/check");

      if (back_data.status !== 200) return;

      let installed_version = this.configStore.data["installed_version"];
      let latest_version = back_data.data.latest;

      this.log("fazendo check de versão...");
      this.log(
        `versão instalada: ${installed_version} versão atualizada: ${latest_version}`
      );
      if (installed_version !== latest_version) {
        this.log("versão desatualizada! atualizando...");
        this.downloadVersion(latest_version);
      }
    },
    async checkLauncherVersion() {
      let version = process.env.VERSION;
      let host = process.env.SERVER_HOST;
      let back_data = await axios.get(host + "/release/check");

      if (back_data.status !== 200) return false;

      if (back_data.data.latest.toString() !== version) {
        this.router.push("/update");
        return true;
      }

      return false;
    },
    async checkConfig() {
      await this.configStore.loadConfig();
      this.log(`config carregada: ${JSON.stringify(this.configStore.data)}`);
    },
    openUpdateChannel() {
      window.eel.open_url(
        "https://discord.com/channels/1251974866551181344/1258338661498490890"
      );
    },
  },
  async mounted() {
    if (window.eel === undefined) {
      return;
    }

    this.log("carregando config...");
    await this.checkConfig();
    this.log("fazendo check do launcher...");
    let shouldUpdate = await this.checkLauncherVersion();

    if (!shouldUpdate) {
      this.log("check do launcher ok.");
      try {
        await this.checkVersion();
      } catch {}
    } else {
      this.log("launcher desatualizado!");
    }
  },
});
</script>

<style>
.Toastify__toast-container {
  /* transform: scale(0.5); */
  zoom: 0.7;
}

.Toastify__toast {
  font-family: "Retropix";
  /* font-size: 11px; */
}
</style>
