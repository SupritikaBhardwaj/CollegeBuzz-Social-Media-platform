import React, { useState } from 'react'

export default function CreatePost({ api, onCreated }) {
  const [content, setContent] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      await api.createPost({ 
        content, 
        image_url: imageUrl, 
        post_type: imageUrl ? 'image' : 'text' 
      })
      setContent('')
      setImageUrl('')
      onCreated?.()
    } catch (e) {
      setError('Failed to create post')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{ maxWidth: 600, margin: '24px auto', padding: 16 }}>
      <div className="hd"><div style={{ fontWeight: 700 }}>Create Post</div></div>
      <form onSubmit={submit} style={{ display:'grid', gap:10 }}>
        <textarea className="input" rows="4" placeholder="What's happening?" value={content} onChange={e => setContent(e.target.value)} />
        <input className="input" placeholder="Image URL (optional)" value={imageUrl} onChange={e => setImageUrl(e.target.value)} />
        {error && <div className="muted" style={{ color:'crimson' }}>{error}</div>}
        <button className="btn" disabled={loading || (!content && !imageUrl)}>{loading ? 'Posting...' : 'Post'}</button>
      </form>
    </div>
  )
}