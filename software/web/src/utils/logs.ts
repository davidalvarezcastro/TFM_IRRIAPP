

export const debug = (fun: string, error: string) => {
  if (import.meta.env.NODE_ENV !== 'production') console.log(fun, error)
}