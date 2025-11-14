const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

export function api(token) {
  const headers = () => ({
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  })

  return {
    // Auth
    async register(payload) {
      const r = await fetch(`${BASE_URL}/auth/register`, { method: 'POST', headers: headers(), body: JSON.stringify(payload) })
      if (!r.ok) throw new Error('Register failed')
      return r.json()
    },
    async login(payload) {
      const r = await fetch(`${BASE_URL}/auth/login`, { method: 'POST', headers: headers(), body: JSON.stringify(payload) })
      if (!r.ok) throw new Error('Login failed')
      return r.json()
    },

    // Posts
    async getFeed() {
      const r = await fetch(`${BASE_URL}/posts/all`)
      if (!r.ok) throw new Error('Failed to load feed')
      return r.json()
    },
    async createPost(payload) {
      const r = await fetch(`${BASE_URL}/posts/create`, { method: 'POST', headers: headers(), body: JSON.stringify(payload) })
      if (!r.ok) throw new Error('Failed to create post')
      return r.json()
    },
    async deletePost(post_id) {
      const r = await fetch(`${BASE_URL}/posts/${post_id}`, { method: 'DELETE', headers: headers() })
      if (!r.ok) throw new Error('Failed to delete post')
      return r.json()
    },
    async getUserPosts(user_id) {
      const r = await fetch(`${BASE_URL}/posts/user/${user_id}`)
      if (!r.ok) throw new Error('Failed to load user posts')
      return r.json()
    },

    // Likes
    async like(post_id) {
      const r = await fetch(`${BASE_URL}/likes/add`, { method: 'POST', headers: headers(), body: JSON.stringify({ post_id }) })
      if (!r.ok) throw new Error('Failed to like')
      return r.json()
    },
    async unlike(post_id) {
      const r = await fetch(`${BASE_URL}/likes/remove`, { method: 'POST', headers: headers(), body: JSON.stringify({ post_id }) })
      if (!r.ok) throw new Error('Failed to unlike')
      return r.json()
    },
    async likeCount(post_id) {
      const r = await fetch(`${BASE_URL}/likes/${post_id}`)
      if (!r.ok) throw new Error('Failed to get like count')
      return r.json()
    },

    // Comments
    async addComment(post_id, comment_text) {
      const r = await fetch(`${BASE_URL}/comments/add`, { method: 'POST', headers: headers(), body: JSON.stringify({ post_id, comment_text }) })
      if (!r.ok) throw new Error('Failed to comment')
      return r.json()
    },
    async getComments(post_id) {
      const r = await fetch(`${BASE_URL}/comments/post/${post_id}`)
      if (!r.ok) throw new Error('Failed to load comments')
      return r.json()
    }
  }
}

// Convenience helper for interactions endpoint
export function interactionsApi(token){
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
  return {
    async share(post_id){
      const r = await fetch(`${BASE_URL}/interactions/share`, { method:'POST', headers, body: JSON.stringify({ post_id }) })
      if (!r.ok) throw new Error('Failed to share')
      return r.json()
    }
  }
}

export function pollsApi(token){
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
  return {
    async create(post_id, question, options){
      const r = await fetch(`${BASE_URL}/polls/create`, { method:'POST', headers, body: JSON.stringify({ post_id, question, options }) })
      if (!r.ok) throw new Error('Failed to create poll')
      return r.json()
    },
    async getForPost(post_id){
      const r = await fetch(`${BASE_URL}/polls/post/${post_id}`)
      if (!r.ok) throw new Error('Failed to load poll')
      return r.json()
    },
    async vote(poll_id, option_index){
      const r = await fetch(`${BASE_URL}/polls/vote`, { method:'POST', headers, body: JSON.stringify({ poll_id, option_index }) })
      if (!r.ok) throw new Error('Failed to vote')
      return r.json()
    },
    async results(poll_id){
      const r = await fetch(`${BASE_URL}/polls/results/${poll_id}`)
      if (!r.ok) throw new Error('Failed to load results')
      return r.json()
    }
  }
}