/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_LICENSE_SERVER: string
  readonly VITE_AGENCIA_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
