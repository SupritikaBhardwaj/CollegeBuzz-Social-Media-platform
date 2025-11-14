import React, { useEffect, useState } from 'react'
import PostCard from './PostCard.jsx'

export default function Feed({ api, currentUser }) {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true
    ;(async () => {
      try {
        const data = await api.getFeed()
        if (mounted) setPosts(data)
      } catch (e) {
        setError('Failed to load feed')
      } finally {
        setLoading(false)
      }
    })()
    return () => { mounted = false }
  }, [api])

  const handleDeletePost = (postId) => {
    setPosts(posts.filter(post => post.post_id !== postId))
  }

  if (loading) return <div className="muted">Loading feed...</div>
  if (error) return <div className="muted" style={{ color: 'crimson' }}>{error}</div>

  return (
    <div>
      {posts.map(p => (
        <PostCard 
          key={p.post_id} 
          post={p} 
          api={api} 
          currentUser={currentUser}
          onDelete={handleDeletePost}
        />
      ))}
      {posts.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '20px' }}>
          <div className="muted">No posts yet. Be the first to post!</div>
        </div>
      )}
    </div>
  )
}