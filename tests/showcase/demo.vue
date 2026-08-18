<template>
  <div class="shuimo-container">
    <!-- Vue 大驼峰组件 (朱砂红加粗高亮测试) -->
    <ShuimoHeader title="水墨·世界" :level="1">
      <template #extra>
        <ShuimoButton type="primary" @click="handleScroll">
          秋水共长天一色
        </ShuimoButton>
      </template>
    </ShuimoHeader>

    <!-- 条件渲染与循环 (Vue 指令与修饰符测试) -->
    <main v-if="isMounted" class="content-wrapper">
      <section v-for="(item, index) in poemList" :key="item.id" class="poem-card">
        <h3 class="poem-title">{{ index + 1 }}. {{ item.title }}</h3>
        <p class="poem-verse">{{ item.verse }}</p>
        <span :class="['tag', item.dynasty]">{{ item.author }} · {{ item.dynasty }}</span>
      </section>
    </main>

    <!-- 骨架屏占位 -->
    <ShuimoSkeleton v-else :loading="isLoading" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';

// 接口与类型定义 (焦墨粗体测试)
export interface PoemItem {
  id: number;
  title: string;
  author: string;
  dynasty: '唐' | '宋' | '元';
  verse: string;
  isFavorite?: boolean;
}

// 响应式状态 (变量与常量测试)
const isLoading = ref<boolean>(false);
const isMounted = ref<boolean>(true);
const MAX_ITEMS: number = 100;

const poemList = reactive<PoemItem[]>([
  {
    id: 1,
    title: '滕王阁序',
    author: '王勃',
    dynasty: '唐',
    verse: '落霞与孤鹜齐飞，秋水共长天一色。'
  },
  {
    id: 2,
    title: '水调歌头',
    author: '苏轼',
    dynasty: '宋',
    verse: '但愿人长久，千里共婵娟。'
  }
]);

// 计算属性与方法 (花青蓝测试)
const totalVerses = computed<number>(() => poemList.length);

function handleScroll(event: MouseEvent): void {
  console.log(`[Shuimo] 点击事件触发，当前诗篇数: ${totalVerses.value}`);
}

onMounted(() => {
  console.log('水墨组件已挂载');
});
</script>

<style scoped>
.shuimo-container {
  background-color: var(--shuimo-bg, #F6F5E1);
  color: #3A3C3F;
  padding: 24px;
}
.poem-title {
  color: #232527;
  font-weight: bold;
}
</style>
