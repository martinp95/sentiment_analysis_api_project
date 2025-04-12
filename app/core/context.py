"""Global application context for shared resources like DB and ML model."""

from typing import Optional

import torch
from motor.motor_asyncio import AsyncIOMotorDatabase
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class AppContext:
    """
    Global container for shared application resources.

    Attributes:
        db (AsyncIOMotorDatabase): MongoDB client instance.
        model (AutoModelForSequenceClassification): Loaded transformer model.
        tokenizer (AutoTokenizer): Tokenizer associated with the model.
        device (torch.device): Device where the model will run (CPU/GPU).
    """

    db: Optional[AsyncIOMotorDatabase] = None
    model: Optional[AutoModelForSequenceClassification] = None
    tokenizer: Optional[AutoTokenizer] = None
    device: Optional[torch.device] = None

    def get_db(self) -> AsyncIOMotorDatabase:
        """
        Get the initialized MongoDB database.

        Returns:
            AsyncIOMotorDatabase: The active database instance.

        Raises:
            RuntimeError: If the database has not been initialized.
        """
        if self.db is None:
            raise RuntimeError("Database connection is not initialized.")
        return self.db

    def get_model(self) -> tuple[AutoModelForSequenceClassification, AutoTokenizer]:
        """
        Get the initialized ML model and tokenizer.

        Returns:
            Tuple: (model, tokenizer)

        Raises:
            RuntimeError: If model or tokenizer are not initialized.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model or tokenizer is not initialized.")
        return self.model, self.tokenizer

    def get_device(self) -> torch.device:
        """
        Get the configured device (CPU or CUDA).

        Returns:
            torch.device: The selected PyTorch device.

        Raises:
            RuntimeError: If device is not set.
        """
        if self.device is None:
            raise RuntimeError("Device is not initialized.")
        return self.device


context = AppContext()
