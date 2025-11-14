import React, { useEffect, useState } from 'react'

export default function AllComments({ api }){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    ;(async () => {
      try {
        const r = await fetch((import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api') + '/comments/all')
        if (!r.ok) throw new Error('Failed')
        const data = await r.json()
        setItems(data)
      } catch(e){
        setError('Failed to load comments')
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  if (loading) return <div className="muted">Loading comments...</div>
  if (error) return <div className="muted" style={{ color:'crimson' }}>{error}</div>

  return (
    <div className="card" style={{ padding: 12 }}>
      <div className="hd"><div style={{ fontWeight:700 }}>All Comments</div></div>
      <div style={{ display:'grid', gap:8, padding:12 }}>
        {items.map(c => (
          <div key={c.comment_id} className="row" style={{ justifyContent:'space-between' }}>
            <div>
              <span style={{ fontWeight:600 }}>{c.username}</span>
              <span className="muted"> on post #{c.post_id}: </span>
              <span>{c.comment_text}</span>
            </div>
            <div className="muted" style={{ fontSize:12 }}>{new Date(c.created_at).toLocaleString()}</div>
          </div>
        ))}
        {items.length === 0 && <div className="muted">No comments yet</div>}
      </div>
    </div>
  )
}


