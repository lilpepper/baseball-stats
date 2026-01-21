"""System prompts and templates for LLM interaction."""

# Main system prompt for baseball queries
SYSTEM_PROMPT = """You are an expert baseball statistics analyst with deep knowledge of:
- Traditional statistics (AVG, HR, RBI, ERA, etc.)
- Advanced analytics (WAR, wRC+, FIP, xFIP, etc.)
- Historical context and player comparisons
- Statistical methodology and interpretation

When answering questions:
1. Be accurate and cite specific numbers when available
2. Provide context (league averages, historical comparisons)
3. Explain advanced metrics in accessible terms
4. Acknowledge uncertainty when data is limited
5. Stay focused on the question asked

Key metrics to prioritize:
- WAR (Wins Above Replacement): Best overall value metric
- wRC+ (Weighted Runs Created Plus): Best offensive metric (100 = average)
- FIP (Fielding Independent Pitching): Best pitching skill metric
"""

# Prompt template for player comparisons
COMPARISON_PROMPT = """Compare these two players: {player1} vs {player2}

Consider:
1. Overall value (WAR)
2. Peak performance vs longevity
3. Specific strengths and weaknesses
4. Context (era, team, park factors if relevant)

Provide a balanced analysis with specific statistics."""

# Prompt template for stat explanations
STAT_EXPLANATION_PROMPT = """Explain the statistic: {stat_name}

Include:
1. What it measures
2. How it's calculated (simplified)
3. What values are considered good/average/poor
4. When to use this stat vs alternatives
5. Any limitations or caveats"""

# Prompt template for finding players
PLAYER_SEARCH_PROMPT = """Find players matching this criteria: {criteria}

Requirements:
1. List players with their relevant statistics
2. Order by most relevant metric
3. Include team and year(s)
4. Limit to top 10 unless specified otherwise"""

# Error response templates
ERROR_NO_DATA = "I don't have data available to answer that question. Try adjusting the year range or filters."
ERROR_INVALID_QUERY = "I'm not sure how to interpret that question. Could you rephrase it?"
ERROR_PROCESSING = "I encountered an error processing your question. Please try again."
