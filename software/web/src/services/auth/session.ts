/**
 * Handle auth token by using cookies (keep session on browser even closing the web app)
 */
import Cookies from 'js-cookie';
import { Session } from '../../types/auth';

export const ACCESS_TOKEN = 'access_token'
export const ID_TOKEN = 'id_token'
export const EXPIRES_AT = 'expires_at'

/**
 * Check if auth info is valid
 */
function isValidSession(): boolean {
    return (
      [ACCESS_TOKEN, ID_TOKEN, EXPIRES_AT].every(
        item => (Cookies.get(item) !== null && Cookies.get(item) !== undefined)
      )
    )
}

/**
 * Store auth info in cookies
 */
export function setSession({ expiresAt, accessToken, idToken }: Session): void {
    Cookies.set(ACCESS_TOKEN, accessToken)
    Cookies.set(ID_TOKEN, idToken)
    // Set the time that the access token will expire at
    Cookies.set(
        EXPIRES_AT,
        JSON.stringify(parseInt(expiresAt) * 1000)
    )
}
  
/**
 * Get auth info from cookies
 */
export function getSession(): Session | null {
    return isValidSession() ? 
        {
            expiresAt: Cookies.get(EXPIRES_AT),
            accessToken: Cookies.get(ACCESS_TOKEN),
            idToken: Cookies.get(ID_TOKEN),
        }
        : null
}

/**
 * Get access token from the session
 */
export function getInfoSession(item: string): string | null {
    return isValidSession() ? 
        Cookies.get(item) : '';
}


/**
 * Remove auth info
 */
export function clearSession(): void {
    // Clear access token and ID token from local storage
    ;[ACCESS_TOKEN, ID_TOKEN, EXPIRES_AT].forEach(item =>
        Cookies.remove(item)
    )
}