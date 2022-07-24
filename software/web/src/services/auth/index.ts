import store from '../../store';
import router from '../../router';
import { User } from '../../types/auth';
import { ACTION_LOGIN, ACTION_LOGOUT, MODULE_AUTH } from '../../store/variables';

/**
 * Try to login using actual auth info stored in vuex
 */
export function tryToLogIn(): boolean {
  // TODO: check token against server (refresh api)
  if (store.getters[`${MODULE_AUTH}/isValidSession`]) return true;

  clearAuth();
  return false;
}

/**
 * Clean session
 */
function clearAuth(): void {
  store.dispatch(`${MODULE_AUTH}/${ACTION_LOGOUT}`);
}

/**
 * Login
 */
export function login(auth: User): Promise<void> {
  return new Promise(async (resolve, reject) => {
    try {
      await store.dispatch(`${MODULE_AUTH}/${ACTION_LOGIN}`, auth);
      router.go(0);
      resolve();
    } catch (error) {
      reject(error);
    }
  })
}

/**
 * Logout
 */
export function logout(): void {
  clearAuth();
  router.go(0);
}
