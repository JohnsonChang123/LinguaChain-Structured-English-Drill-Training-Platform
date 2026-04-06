import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { login, register } from '../lib/api'

export function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('student@example.com')
  const [password, setPassword] = useState('password123')
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [error, setError] = useState('')

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')

    try {
      const result = mode === 'login' ? await login(email, password) : await register(email, password)
      localStorage.setItem('token', result.access_token)
      navigate('/courses')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Request failed')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 bg-white p-6 rounded-xl shadow space-y-4">
      <h1 className="text-2xl font-bold">FSI English Training MVP</h1>
      <p className="text-sm text-slate-600">Login or register to start drills.</p>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded p-2" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input className="w-full border rounded p-2" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">{mode === 'login' ? 'Login' : 'Register'}</button>
      </form>
      <button className="text-sm underline" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
        Switch to {mode === 'login' ? 'register' : 'login'}
      </button>
    </div>
  )
}
