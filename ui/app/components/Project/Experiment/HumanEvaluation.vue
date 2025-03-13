<script setup lang="ts">
import type { FormSubmitEvent } from '@nuxt/ui'
import { HumanEvalSchema } from '~~/shared/types/humaneval.type'
import { useMutation } from '@tanstack/vue-query';


const route = useRoute()
const loading = ref(false)


const { mutate } = useMutation({
    mutationFn: async (data: any) => {
        return useHumanEvalQueryExperiments(experimentIds.value, data)
    },
    onSuccess: (data) => {
        experimentsData.value = data.results
        loading.value = false
    }
})


const experimentsData = ref([]);

const experimentIds = computed(() => {
  const experiments = route.query.experiments
  return typeof experiments === 'string' ? experiments.split(',') : []
})



const questionAsked = ref('')
const showResponses = ref(false)

const state = reactive<Partial<HumanEval>>({
  message: undefined,
})

const toast = useToast()
async function onSubmit(event: FormSubmitEvent<HumanEval>) {
  toast.add({ title: 'Success', description: 'The form has been submitted.', color: 'success' })
  console.log(event.data)
  mutate(event.data)
}

const {mutate: upvote} = useMutation({
    mutationFn: async (data: any) => {
        return useHumanEvalUpvote(data)
    }
})

const experimentId = ref('')

const approveExample = (id: string) => {
  experimentId.value = id;
  const data = experimentIds.value.reduce((acc: Record<string, number>, expId: string) => {
    acc[expId] = expId === id ? 1 : 0;
    return acc;
  }, {});
  upvote(data)
}


const sendMessage = (e) => {
  loading.value = true
  questionAsked.value = e.data.message
  mutate(e.data.message)
  state.message = ''
  experimentId.value = '';
  showResponses.value = true
}


const items = ref([]);

items.value = [{
    label: 'Experiment Details',
    icon: 'i-lucide-info'
}]


</script>

<template>
  <div class="h-[calc(100vh-200px)] mt-5">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Human Evaluation</h1>
      <UButton class="secondary-btn" :to="{name: 'projects-id-experiments', query: {experiments: experimentIds.join(',')}}">
        See Results
        <UIcon name="i-lucide-arrow-right" />
      </UButton>
    </div>
    <div :class="[
      'border-2 border-gray-300 rounded-md p-2 h-[15%] mt-5 transition-all duration-500',
      {
        'transform translate-y-0 relative top-[30%]': !questionAsked,
        'transform relative top-[0%]': questionAsked,

      }
    ]">
      <UForm :schema="HumanEvalSchema" :state="state" class="flex justify-between items-center h-full" @submit="sendMessage">
        <UFormField :ui="{error: 'ml-2'}" name="message" class="w-full m-0">
          <UInput v-model="state.message" placeholder="Enter your question" class="input-box h-full m-0" :ui="{
          base: 'test h-full!'
        }">
    <template #trailing>
        <UButton :disabled="!state.message || state.message.length < 10" class="primary-bg-color aws-font-grey-color" icon="i-lucide-send" type="submit"></UButton>
    </template>
    
    </UInput>
        </UFormField>

      </UForm>
    </div>
    <Transition v-if="loading" name="fade">
        <div class="flex justify-center items-center h-full">
            <UIcon name="i-lucide-loader-circle" class="animate-spin" size="120" />
          <!-- <UProgress :ui="{track: 'bg-gray-300', filled: 'bg-primary-color'}" :value="50" /> -->
        </div>
    </Transition>
    
    <Transition v-else name="fade">
      <div v-if="questionAsked && showResponses" class="border-2 border-gray-300 rounded-md p-2 h-[70%] mt-5 pb-14 pt-3">
        <div class="flex justify-start items-center mb-5">
            <UBadge class="mr-2" variant="solid" color="neutral">
                Question:
            </UBadge>
            <h1 class="font-bold">{{ questionAsked.length > 100 ? questionAsked.slice(0, 97) + '...' : questionAsked }}</h1>
            <UModal class="max-h-[400px]" v-if="questionAsked.length > 100" title="Question">
                <UButton class="secondary-color ml-5" label="View Question" color="neutral" variant="ghost" />

                <template #body>
                <p class="h-full max-h-[150px] overflow-y-auto">{{ questionAsked }}</p>
                </template>
            </UModal>
        </div>
        <div v-if="!loading" class="flex justify-around h-full pb-5">
          <UCard v-for="experiment in experimentsData" :key="experiment.id" class="p-4" :ui="{root:'overflow-y-auto'}" :class="{'w-[30%]': experimentsData.length === 3, 'w-[45%]': experimentsData.length === 2}">
            <template #header>
              <div class="flex justify-between mt-2 items-start">
                <div>
                  <UBadge>
                    <p>{{ experiment.experiment_id }}</p>
                  </UBadge>
                  <UAccordion :items="items">
                    <template #body="{ item }">
                      <div class="overflow-y-auto max-h-[100px] scrollbar-hide" v-for="(value, key) in experiment.metadata">
                          <strong>{{ key }}:</strong> {{ value }}
                      </div>
                    </template>
                  </UAccordion>
                </div>
                <UButton v-if="experiment.experiment_id !== experimentId" class="primary-btn" @click="approveExample(experiment.experiment_id)" :disabled="experimentId !== experiment.experiment_id && experimentId !== ''">
                  <UIcon name="i-lucide-thumbs-up" />
                </UButton>
                <UBadge color="success" v-else>
                  <UIcon name="i-lucide-check" />
                </UBadge>
              </div>
            </template>
            <template #default>
              <div class="overflow-y-auto max-h-[400px] p-4">
                {{ experiment.answer}}
              </div>
            </template>
          </UCard>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.input-box {
  /* border: 1px solid #e0e0e0;
  border-radius: 5px; */
  padding: 10px;
}

.input-box > input {
  height: 52px !important;
  width: 100% !important;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

.duration-500 {
  transition-duration: 500ms;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>