from pydantic import BaseModel

class UserProfile(BaseModel):
    name: str
    age: int
    occupation: str
    zodiac_sign: str
    selected_character: str = "Ana Karakter" # Kullanıcı kimi replace edecek?

    def __str__(self):
        return f"{self.name} ({self.age}), {self.occupation}, {self.zodiac_sign} burcu."