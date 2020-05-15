<template>
  <el-menu :router="true" background-color="#EDEDED" text-color="#909399" active-text-color="#212529">
    <el-menu-item index="./overview">
      <span>Overview</span>
    </el-menu-item>
    <el-menu-item index="2">
      <span>Project</span>
    </el-menu-item>
    <el-menu-item index="3">
      <span>Sprint</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  data () {
    return {
      tabPosition: 'left'
    }
  }
}
</script>

<style scoped lang="scss">

  .el-menu {
    height: 100%;
    text-align: left;
  }

  .el-menu-item {
    font-size: 16px;
  }

</style>
