<template>
  <div>
    <div v-if="this.$route.path.id" class="warning">
      check and EDIT PROJECT info
    </div>
    <div v-else>
      <div class="primary">
        Hi, do you wanna ADD new PROJECT
      </div>
    </div>
  </div>
</template>
