<template>
  <div class="flex flex-center update-container">
    <div>
      <p style="font-size: 12px">atualize seu launcher!</p>
      <p style="font-size: 10px; color: #eee">
        saiu uma atualização direto do forno pra você!!! <br />
        nosso programa atualizador deve abrir a qualquer instante e irá fazer
        tudo automagicamente...
        <br /><br />
        caso algo deu errado, faça um bug report no servidor de discord!
      </p>
    </div>
  </div>
</template>

<script setup>
import { usePlayerStore } from "src/stores/player";
import { onMounted } from "vue";

const playerStore = usePlayerStore();
playerStore.isLoading = false;

onMounted(() => {
  setTimeout(() => {
    if (window.eel == undefined) return;
    window.eel.trigger_update();
  }, 1000);
});
</script>

<style>
.update-container {
  width: 100%;
  height: 400px;
  padding: 100px;
}

.update-container p {
  text-align: center;
}

span.dscrd {
  background: rgb(6, 6, 6);
  padding: 3px;
  border-radius: 5px;
  color: #ccc;
  font-weight: bold;
  cursor: pointer;
}
</style>
