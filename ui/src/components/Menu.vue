<template>
  <el-menu
    :router="true"
    :default-active="1"
    background-color="#EDEDED"
    text-color="#909399"
    active-text-color="#212529">
    <el-menu-item-group title="Dashboard" style="margin-top: 15px;">
    <el-menu-item index="1" route="/overview">
      <span style="margin-left: 15px;">Overview</span>
    </el-menu-item>
    <el-menu-item index="2" route="/project">
      <span style="margin-left: 15px;">Project</span>
    </el-menu-item>
    <el-menu-item index="3" route="/sprint">
      <span style="margin-left: 15px;">Sprint</span>
    </el-menu-item>
    </el-menu-item-group>
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
