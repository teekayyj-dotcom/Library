from pydantic import BaseModel
from typing import List

class ImportResponse(BaseModel):
    total_processed: int
    successful_imports: int
    failed_imports: int
    error_messages: List[str]
