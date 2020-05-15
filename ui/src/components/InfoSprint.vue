<template>
  <div>
    <el-button v-if="this.$route.path.id" class="warning">
      check and EDIT SPRINT info
    </el-button>
    <div v-else>
      <el-button class="primary">
        Hi, do you wanna ADD new SPRINT
      </el-button>
    </div>
  </div>
</template>
