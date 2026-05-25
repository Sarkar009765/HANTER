from __future__ import annotations

from typing import List, Dict


class ConversationSummarizer:
    async def compress(self, messages: List[Dict]) -> str:
        if len(messages) <= 10:
            return self._format_messages(messages)

        old_messages = messages[:-10]
        recent_messages = messages[-10:]
        summary = self._simple_summarize(old_messages)
        return f"[Summary: {summary}]\n\n{self._format_messages(recent_messages)}"

    def _format_messages(self, messages: List[Dict]) -> str:
        return "\n".join(
            f"{m.get('role', 'unknown')}: {m.get('content', '')}"
            for m in messages
        )

    def _simple_summarize(self, messages: List[Dict]) -> str:
        content = " ".join(
            m.get("content", "") for m in messages if m.get("role") != "system"
        )
        if len(content) > 500:
            return content[:500] + "..."
        return content
