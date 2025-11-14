import React, { useEffect, useMemo, useState } from 'react'
import { api } from './lib/api.js'
import Feed from './components/Feed.jsx'
import AllComments from './components/AllComments.jsx'
import Login from './components/Login.jsx'
import Register from './components/Register.jsx'
import CreatePost from './components/CreatePost.jsx'

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem('token') || '')
  const [currentUser, setCurrentUser] = useState(() => {
    const user = localStorage.getItem('currentUser')
    return user ? JSON.parse(user) : null
  })
  const [view, setView] = useState('feed')

  const authedApi = useMemo(() => api(token), [token])

  const handleLoginSuccess = (newToken, userData) => {
    localStorage.setItem('token', newToken)
    localStorage.setItem('currentUser', JSON.stringify(userData))
    setToken(newToken)
    setCurrentUser(userData)
    setView('feed')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('currentUser')
    setToken('')
    setCurrentUser(null)
    setView('login')
  }

  useEffect(() => {
    if (!token) setView('login')
  }, [token])

  return (
    <>
      <div className="nav">
        <div className="nav-inner">
          <div className="brand">CollegeBuzz</div>
          <div className="row">
            {token && (
              <>
                <div className="muted" style={{ marginRight: '10px' }}>
                  Welcome, {currentUser?.name || 'User'}!
                </div>
                <button className="btn secondary" onClick={() => setView('feed')}>Feed</button>
                <button className="btn secondary" onClick={() => setView('create')}>Create</button>
                <button className="btn secondary" onClick={() => setView('comments')}>Comments</button>
                <button className="btn" onClick={handleLogout}>Logout</button>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="container">
        {!token && view === 'login' && (
          <Login 
            onSuccess={handleLoginSuccess}
            onGoRegister={() => setView('register')} 
          />
        )}
        {!token && view === 'register' && (
          <Register onSuccess={() => setView('login')} onGoLogin={() => setView('login')} />
        )}

        {token && view === 'feed' && (
          <Feed api={authedApi} currentUser={currentUser} />
        )}

        {token && view === 'create' && (
          <CreatePost api={authedApi} onCreated={() => setView('feed')} />
        )}

        {token && view === 'comments' && (
          <AllComments api={authedApi} />
        )}
      </div>
    </>
  )
}