"""Application-wide context container."""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase


class AppContext:
    """
    Application context for managing shared resources.

    Attributes:
        db (AsyncIOMotorDatabase): MongoDB database instance.
    """

    db: Optional[AsyncIOMotorDatabase] = None

    def get_db(self) -> AsyncIOMotorDatabase:
        """
        Retrieve the MongoDB database instance.

        Returns:
            AsyncIOMotorDatabase: The MongoDB database instance.
        """
        if self.db is None:
            raise RuntimeError("Database connection is not initialized.")
        return self.db


context = AppContext()
