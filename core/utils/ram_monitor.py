from __future__ import annotations

import psutil
import gc
import asyncio
from typing import Optional, Callable
from utils.logger import logger


class RAMMonitor:
    def __init__(self, threshold_mb: int = 1800, emergency_threshold_mb: int = 200):
        self.threshold = threshold_mb
        self.emergency_threshold = emergency_threshold_mb
        self.process = psutil.Process()
        self._emergency_callbacks: list[Callable] = []

    def on_emergency(self, callback: Callable):
        self._emergency_callbacks.append(callback)

    async def check(self) -> dict:
        mem = self.process.memory_info()
        used_mb = mem.rss / 1024 / 1024
        available_mb = psutil.virtual_memory().available / 1024 / 1024
        total_mb = psutil.virtual_memory().total / 1024 / 1024

        status = {
            "used_mb": round(used_mb, 1),
            "available_mb": round(available_mb, 1),
            "total_mb": round(total_mb, 1),
            "percent": round(psutil.virtual_memory().percent, 1),
            "level": "normal"
        }

        if used_mb > self.threshold:
            status["level"] = "warning"
            logger.warning("ram_high_usage", used_mb=used_mb, threshold=self.threshold)

        if available_mb < self.emergency_threshold:
            status["level"] = "emergency"
            logger.critical("ram_emergency", available_mb=available_mb)
            await self._trigger_emergency()

        return status

    async def _trigger_emergency(self):
        gc.collect()
        for callback in self._emergency_callbacks:
            try:
                await callback()
            except Exception as e:
                logger.error("ram_emergency_callback_error", error=str(e))


class RAMOptimizer:
    def __init__(self, monitor: RAMMonitor):
        self.monitor = monitor
        self._is_emergency_mode = False

    @property
    def is_emergency_mode(self) -> bool:
        return self._is_emergency_mode

    async def optimize(self, skill_loader=None, memory_manager=None):
        status = await self.monitor.check()
        level = status["level"]

        if level == "emergency" and not self._is_emergency_mode:
            self._is_emergency_mode = True
            if skill_loader:
                skill_loader.unload_all_non_essential()
            if memory_manager:
                memory_manager.clear_cache()
            gc.collect()
            logger.info("ram_emergency_mode_activated")
        elif level == "normal" and self._is_emergency_mode:
            self._is_emergency_mode = False
            logger.info("ram_normal_mode_restored")
