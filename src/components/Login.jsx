import React, { useState } from 'react'
import { api as makeApi } from '../lib/api.js'

export default function Login({ onSuccess, onGoRegister }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const api = makeApi('')

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await api.login({ email, password })
      onSuccess(res.token, res.user) // Pass user data along with token
    } catch (err) {
      setError('Login failed - check your credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{ maxWidth: 420, margin: '32px auto', padding: 16 }}>
      <div className="hd"><div className="brand">Login</div></div>
      <form onSubmit={submit} style={{ display: 'grid', gap: 10 }}>
        <input className="input" type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
        <input className="input" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        {error && <div className="muted" style={{ color: 'crimson' }}>{error}</div>}
        <button className="btn" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
      </form>
      <div style={{ padding: 12 }}>
        <span className="muted">No account?</span> <a href="#" onClick={(e) => { e.preventDefault(); onGoRegister() }}>Register</a>
      </div>
    </div>
  )
}