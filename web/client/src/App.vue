<template>
    <div v-if="store.getters.initialized">
        <div class="inner">
            <router-view v-slot="{ Component }">
                <component :is="Component" />
            </router-view>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";

import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()


onMounted(() => {
    store.commit('init')
});

</script>
