from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at = db.Column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
)

    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    favorite_starships: Mapped[list["FavoriteStarship"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    species: Mapped[str] = mapped_column(String(50))

    favorited_by: Mapped[list["FavoriteCharacter"]] = relationship(
        back_populates="character"
    )

class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    population: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))

    favorited_by: Mapped[list["FavoritePlanet"]] = relationship(
        back_populates="planet"
    )

class Starship(db.Model):
    __tablename__ = "starship"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100))
    manufacturer: Mapped[str] = mapped_column(String(100))
    crew: Mapped[str] = mapped_column(String(50))

    favorited_by: Mapped[list["FavoriteStarship"]] = relationship(
        back_populates="starship"
    )

class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(back_populates="favorited_by")


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorited_by")


class FavoriteStarship(db.Model):
    __tablename__ = "favorite_starship"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    starship_id: Mapped[int] = mapped_column(ForeignKey("starship.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_starships")
    starship: Mapped["Starship"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
