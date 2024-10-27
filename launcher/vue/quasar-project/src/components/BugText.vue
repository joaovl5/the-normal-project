<template>
  <p>
    {{ bug_text }}
  </p>
</template>

<script>
import { ref } from "vue";

export default {
  props: ["value"],
  setup(props) {
    const bug_text = ref(props.value);

    function listUtfCharacters(start, end) {
      let characters = [];
      for (let i = start; i <= end; i++) {
        characters.push(String.fromCharCode(i));
      }
      return characters;
    }
    let alphabet = listUtfCharacters(33, 126).concat(
      listUtfCharacters(170, 250)
    );

    setInterval(() => {
      bug_text.value = bug_text.value
        // .toString()
        .split("")
        .map((c) =>
          c == " " ? " " : alphabet[Math.floor(Math.random() * alphabet.length)]
        )
        .join("");
    }, 35);

    return { bug_text };
  },
};
</script>
