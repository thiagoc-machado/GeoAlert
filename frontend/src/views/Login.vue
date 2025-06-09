<template>
  <div class="login-container">
    <h1>🔐 Login</h1>
    <p class="subtitle">Access your account to manage and view geographic alerts.</p>

    <form @submit.prevent="submit" class="login-form">
      <input
        v-model="username"
        placeholder="Username"
        required
        class="form-input"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
        class="form-input"
      />
      <button type="submit" class="btn primary">Login</button>
    </form>

    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  methods: {
    ...mapActions(['login']),
    async submit() {
      try {
        await this.login({ username: this.username, password: this.password })
        this.$router.push('/alerts-map')
      } catch (err) {
        this.error = 'Invalid credentials. Please try again.'
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 5rem auto;
  padding: 2rem;
  border-radius: 12px;
  background-color: #ffffffd9;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-input {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px #3498db30;
}

.error-message {
  margin-top: 1rem;
  color: #e74c3c;
  font-weight: bold;
}
</style>
