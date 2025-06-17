import { createStore } from "vuex";
import axios from "../axios";
import { keycloak } from "../keycloak";

export default createStore({
    state: {
        token: localStorage.getItem("token") || null,
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
            localStorage.setItem("token", token);
        },
        clearToken(state) {
            state.token = null;
            localStorage.removeItem("token");
        },
    },
    actions: {
        async login({ commit }, credentials) {
            // login manual desativado, pois Keycloak faz o login automaticamente
            console.warn(
                "manual login is disabled, Keycloak handles authentication automatically"
            );
        },
        logout({ commit }) {
            commit("clearToken");
            keycloak.logout({
                redirectUri: window.location.origin + "/",
            });
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
});
