<template>
  <el-menu
    :router="true"
    :default-active="activeIndex2"
    @select="handleSelect"
    mode="horizontal"
    background-color="#212529"
    text-color="#909399"
    active-text-color="#fff">
    <el-menu-item>
      <a class="nav-brand" style="display: inline-block; color: #fff; font-size: 1.75em;">
        <img src="/logo.png" width="38px;" style="margin: -20px; margin-top: -25px;">
        <a style="margin: 20px;">sphere</a>
      </a>
    </el-menu-item>
    <el-menu-item index="1" route="/">
      <i class="el-icon-odometer" style="font-size: 1.25em"></i>
      <span>Dashboard</span>
    </el-menu-item>
    <el-menu-item index="2" route="/settings">
      <i class="el-icon-setting" style="font-size: 1.25em"></i>
      <span>Settings</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  data () {
    return {
      activeIndex: '1',
      activeIndex2: '1'
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style scoped lang="scss">

  .el-menu-item {
    font-size: 16px;
  }

</style>
