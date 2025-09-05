"""
Module for AI improve.
"""


class AIService:
    """
    A service for interacting with AI models (or their stubs).
    """

    async def improve_resume_content(self, original_content: str) -> str:
        """
        Accepts the original content, and returns an improved version.
        Args:
            original_content (str): Text for improvement.

        Returns:
            str: Text of improved content
        """
        improved_content = f"{original_content} [Improved]"

        return improved_content


ai_service = AIService()
