<script setup lang="ts">
import { notify } from "@kyvg/vue3-notification";
import { ref, onMounted, Ref, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { login } from "../../services/auth";
import { User } from "../../types/auth";

name: "LoginView";

const router = useRouter();

onMounted(async () => {});

onBeforeUnmount(async () => {});

const valid = ref(true);
const submitting = ref(false);
const formName = ref(null);
const username: Ref<string | null> = ref(null);
const password: Ref<string | null> = ref(null);
const viewPassword = ref(false);

/**
 * Form methods
 */
const validate = () => {
  formName.value.validate();
};

const changeVisibility = () => {
  viewPassword.value = !viewPassword.value;
};

const handleReset = () => {
  formName.value.reset();
};

const handleLogin = async () => {
  validate();

  const cb = () => {
    submitting.value = false;
  };

  if (valid.value) {
    submitting.value = true;

    try {
      await login({
        user: username.value,
        password: password.value,
      } as User);
    } catch (err) {
      notify({
        title: "Login error",
        text: err,
        type: "error",
      });
    }
    cb();
  }
};
</script>

<template>
  <div class="container">
    <v-card class="login">
      <v-card-title class="title-container">
        <p class="title">IrriApp Login</p>
      </v-card-title>

      <v-card-text class="content">
        <v-form ref="formName" v-model="valid" lazy-validation>
          <v-text-field
            v-model="username"
            prepend-icon="mdi-account"
            :rules="[(v) => !!v || 'Username is required']"
            label="Username"
            required
            clearable
          />
          <v-text-field
            v-model="password"
            prepend-icon="mdi-lock"
            :append-inner-icon="viewPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :type="viewPassword ? 'text' : 'password'"
            :rules="[(v) => !!v || 'Password is required']"
            label="Password"
            required
            clearable
            @click:append-inner="changeVisibility"
          />

          <div class="operations">
            <v-btn
              color="grey"
              prepend-icon="mdi-delete"
              class="mr-4"
              @click="handleReset"
            >
              Reset
            </v-btn>

            <v-btn color="success" @click="handleLogin"> Login </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<style lang="scss" scoped>
.container {
  min-height: 100%;
  width: 100%;
  background-color: #fafafa;
  overflow: hidden;

  .login {
    width: 520px;
    margin: 0 auto;
    overflow: hidden;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    .title-container {
      background-color: grey;
      height: 75px;

      .title {
        font-size: 26px;
        color: white;
        margin: 0px;
        font-weight: bold;
        line-height: 60px;
      }
    }

    .content {
      padding: 50px 25px;

      .operations {
        display: flex;
        justify-content: right;
      }
    }
  }
}
</style>
