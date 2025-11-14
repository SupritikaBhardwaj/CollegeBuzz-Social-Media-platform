import { createPoll, getPollByPost, votePoll, getPollResults } from "../models/poll.js";

export const createPollController = async (req, res) => {
  try {
    const { post_id, question, options } = req.body;
    if (!post_id || !question || !Array.isArray(options) || options.length < 2)
      return res.status(400).json({ error: "Invalid poll payload" });
    
    const pollId = await createPoll(post_id, question, options.slice(0,4));
    res.status(201).json({ poll_id: pollId });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Failed to create poll" });
  }
};

export const getPollForPost = async (req, res) => {
  try {
    const { post_id } = req.params;
    const poll = await getPollByPost(post_id);
    if (!poll) return res.status(404).json({ message: "No poll for this post" });
    res.json(poll);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Failed to fetch poll" });
  }
};

export const voteOnPoll = async (req, res) => {
  try {
    const { poll_id, option_index } = req.body;
    const user_id = req.user.id; // Get user_id from authenticated token
    
    if (![0,1,2,3].includes(Number(option_index))) return res.status(400).json({ error: "Invalid option" });
    await votePoll(poll_id, user_id, Number(option_index));
    res.json({ message: "Vote recorded" });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Failed to vote" });
  }
};

export const getResults = async (req, res) => {
  try {
    const { poll_id } = req.params;
    const rows = await getPollResults(poll_id);
    res.json(rows);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Failed to get results" });
  }
};