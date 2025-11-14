import React, { useEffect, useState } from 'react'
import { interactionsApi, pollsApi } from '../lib/api.js'

export default function PostCard({ post, api, currentUser, onDelete }) {
  const [likeCount, setLikeCount] = useState(0)
  const [commentText, setCommentText] = useState('')
  const [comments, setComments] = useState([])
  const [commentsLoading, setCommentsLoading] = useState(false)
  const [commentsError, setCommentsError] = useState('')
  const [showComments, setShowComments] = useState(false)
  const [poll, setPoll] = useState(null)
  const [selected, setSelected] = useState(null)

  const interApi = interactionsApi(localStorage.getItem('token'))
  const pApi = pollsApi(localStorage.getItem('token'))

  useEffect(() => {
    ;(async () => {
      try {
        const c = await api.likeCount(post.post_id)
        setLikeCount(c.like_count || 0)
        const list = await api.getComments(post.post_id)
        setComments(list)
        try {
          const pol = await pApi.getForPost(post.post_id)
          if (pol && pol.poll_id) setPoll(pol)
        } catch {}
      } catch {}
    })()
  }, [post.post_id, api])

  const doLike = async () => {
    await api.like(post.post_id)
    const c = await api.likeCount(post.post_id)
    setLikeCount(c.like_count || 0)
  }

  const submitComment = async (e) => {
    e.preventDefault()
    if (!commentText.trim()) return
    await api.addComment(post.post_id, commentText.trim())
    setCommentText('')
    const list = await api.getComments(post.post_id)
    setComments(list)
  }

  const doShare = async () => {
    try {
      await interApi.share(post.post_id)
      alert('Post shared!')
    } catch (e) {
      alert('Failed to share')
    }
  }

  const doDelete = async () => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      try {
        await api.deletePost(post.post_id)
        onDelete?.(post.post_id)
        alert('Post deleted successfully!')
      } catch (error) {
        alert('Failed to delete post')
      }
    }
  }

  const doVote = async () => {
    if (selected === null) return
    try {
      await pApi.vote(poll.poll_id, selected)
      alert('Vote recorded!')
    } catch (error) {
      alert('Failed to vote')
    }
  }

  useEffect(() => {
    let mounted = true
    setCommentsLoading(true)
    setCommentsError('')
    api.getComments(post.post_id)
      .then(list => { if (mounted) setComments(list) })
      .catch(() => { if (mounted) setCommentsError('Failed to load comments') })
      .finally(() => { if (mounted) setCommentsLoading(false) })
    return () => { mounted = false }
  }, [post.post_id, api])

  // Check if current user is the post owner
  const isPostOwner = currentUser && currentUser.user_id === post.user_id

  return (
    <div className="card">
      <div className="hd">
        <div className="avatar" />
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600 }}>{post.username || 'User'}</div>
          <div className="muted">Post #{post.post_id}</div>
        </div>
        {isPostOwner && (
          <button 
            className="btn secondary" 
            onClick={doDelete}
            style={{ background: 'transparent', color: 'crimson', border: '1px solid crimson' }}
          >
            🗑️ Delete
          </button>
        )}
      </div>
      
      {post.image_url && (
        <img className="post-img" src={post.image_url} alt="post" />
      )}
      
      <div style={{ padding: 12 }}>{post.content}</div>
      
      {poll && (
        <div style={{ padding: '0 12px 12px' }}>
          <div style={{ fontWeight:600, marginBottom:8 }}>{poll.question}</div>
          {[poll.option1, poll.option2, poll.option3, poll.option4].filter(Boolean).map((opt, idx) => (
            <label key={idx} className="row" style={{ gap:6, marginBottom:6 }}>
              <input type="radio" name={`poll-${poll.poll_id}`} checked={selected===idx} onChange={() => setSelected(idx)} /> {opt}
            </label>
          ))}
          <button className="btn" onClick={doVote} disabled={selected === null}>
            Vote
          </button>
        </div>
      )}
      
      <div className="actions">
        <button className="btn secondary" onClick={doLike}>❤ Like ({likeCount})</button>
        <button className="btn secondary" onClick={doShare}>↗ Share</button>
        <button className="btn secondary" onClick={() => setShowComments(v => !v)}>
          💬 {showComments ? 'Hide' : 'Show'} comments ({comments.length})
        </button>
      </div>
      
      {showComments && (
        <div style={{ padding: '0 12px 12px' }}>
          <div style={{ marginBottom: 8, fontWeight: 600 }}>Comments</div>
          {commentsLoading && <div className="muted">Loading comments...</div>}
          {commentsError && <div className="muted" style={{ color:'crimson' }}>{commentsError}</div>}
          <div style={{ display: 'grid', gap: 6, marginBottom: 10 }}>
            {comments.map(c => (
              <div key={c.comment_id} className="row" style={{ justifyContent: 'space-between' }}>
                <div><span style={{ fontWeight: 600 }}>{c.username}</span> <span className="muted">{c.comment_text}</span></div>
                <div className="muted" style={{ fontSize: 12 }}>{new Date(c.created_at).toLocaleString()}</div>
              </div>
            ))}
            {comments.length === 0 && <div className="muted">No comments yet</div>}
          </div>
          <form onSubmit={submitComment} className="row">
            <input 
              className="input" 
              placeholder="Add a comment..." 
              value={commentText} 
              onChange={e => setCommentText(e.target.value)} 
            />
            <button className="btn">Post</button>
          </form>
        </div>
      )}
    </div>
  )
}