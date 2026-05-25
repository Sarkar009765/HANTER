from __future__ import annotations

import os
from typing import Optional, AsyncGenerator, List
from models import IntentClassification, IntentType
from utils.logger import logger


class LLMClient:
    def __init__(self):
        self._provider = None
        self._model = None
        self._client = None
        self._initialize()

    def _initialize(self):
        groq_key = os.getenv("GROQ_API_KEY")
        together_key = os.getenv("TOGETHER_API_KEY")

        if groq_key:
            self._provider = "groq"
            self._model = "llama-3.1-8b-instant"
            self._api_key = groq_key
            logger.info("llm_initialized", provider="groq")
        elif together_key:
            self._provider = "together"
            self._model = "qwen-2.5-7b-instruct"
            self._api_key = together_key
            logger.info("llm_initialized", provider="together")
        else:
            self._provider = "mock"
            logger.warning("llm_no_api_key", message="Running in mock mode. Set GROQ_API_KEY or TOGETHER_API_KEY")

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, stream: bool = False) -> str:
        if self._provider == "mock":
            return self._mock_response(prompt)

        try:
            return await self._litellm_generate(prompt, system_prompt, stream)
        except Exception as e:
            logger.error("llm_generation_error", error=str(e))
            return self._mock_response(prompt)

    async def _litellm_generate(self, prompt: str, system_prompt: Optional[str] = None, stream: bool = False) -> str:
        try:
            import litellm
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = await litellm.acompletion(
                model=f"{self._provider}/{self._model}" if self._provider != "mock" else "gpt-3.5-turbo",
                messages=messages,
                max_tokens=4096,
                temperature=0.7,
                api_key=self._api_key
            )
            return response.choices[0].message.content or ""
        except ImportError:
            return self._mock_response(prompt)

    async def classify_intent(self, text: str) -> IntentClassification:
        prompt = f"""Classify this user message into one of these intents:
- CODE_GENERATION: Writing, editing, debugging code
- PROJECT_SCAFFOLD: Creating new project structure
- DEPLOYMENT: Deploying to hosting platforms
- SOCIAL_MEDIA: Creating or scheduling social content
- WEB_RESEARCH: Searching, scraping, monitoring websites
- FILE_ORGANIZATION: Managing local files
- SYSTEM_AUTOMATION: Automating OS tasks
- GENERAL_CHAT: Casual conversation or questions

User message: {text}

Respond ONLY with the intent name."""

        response = await self.generate(prompt)
        response = response.strip().upper()

        for intent in IntentType:
            if intent.value in response:
                return IntentClassification(
                    intent=intent,
                    confidence=0.85,
                    emotion="neutral",
                    entities=[]
                )

        return IntentClassification(
            intent=IntentType.GENERAL_CHAT,
            confidence=0.7,
            emotion="neutral",
            entities=[]
        )

    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None) -> AsyncGenerator[str, None]:
        response = await self.generate(prompt, system_prompt)
        words = response.split()
        for word in words:
            yield word + " "
            import asyncio
            await asyncio.sleep(0.05)

    def _mock_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "deploy" in prompt_lower:
            return "I'll help you deploy that project. Let me check the build status and push to production."
        if "create" in prompt_lower or "build" in prompt_lower or "scaffold" in prompt_lower:
            return "I'll set up the project structure and scaffold the initial code. What template would you like to use?"
        if "search" in prompt_lower or "find" in prompt_lower:
            return "Let me search for that information. I'll scan the web and compile the results."
        if "organize" in prompt_lower or "clean" in prompt_lower:
            return "I'll organize those files for you. Let me scan the directory structure first."
        if "tweet" in prompt_lower or "post" in prompt_lower or "social" in prompt_lower:
            return "I'll draft some engaging social media content for you. What's the topic?"
        if "monitor" in prompt_lower or "system" in prompt_lower:
            return "I'll check your system metrics and optimize performance."
        return f"I understand you want to: {prompt[:100]}. Let me work on that."
