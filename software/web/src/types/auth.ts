export type User = {
  user: string,
  password: string
}

export type Session = {
  expiresAt: string,
  accessToken: string,
  idToken: string,
  user?: User | null
}
