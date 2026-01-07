from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False
    )

    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(
        "FavoriteCharacter",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(
        "FavoritePlanet",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    favorite_starships: Mapped[list["FavoriteStarship"]] = relationship(
        "FavoriteStarship",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f'Usuario {self.email}'
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    height: Mapped[int] = mapped_column(Integer())

    favorited_by: Mapped[list["FavoriteCharacter"]] = relationship(
        "FavoriteCharacter",
        back_populates="character",
    )

    def __repr__(self):
        return f'Personaje {self.name}'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height
        }



class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    climate: Mapped[str] = mapped_column(String(50))

    population: Mapped[str] = mapped_column(String(50))

    terrain: Mapped[str] = mapped_column(String(50))

    favorited_by: Mapped[list["FavoritePlanet"]] = relationship(
        "FavoritePlanet",
        back_populates="planet",
    )

    def __repr__(self):
        return f'Planeta {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'population': self.population,
            'terrain': self.terrain
        }


class Starship(db.Model):
    __tablename__ = "starship"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    model: Mapped[str] = mapped_column(String(100))

    manufacturer: Mapped[str] = mapped_column(String(100))

    crew: Mapped[str] = mapped_column(String(50))

    favorited_by: Mapped[list["FavoriteStarship"]] = relationship(
        "FavoriteStarship",
        back_populates="starship",
    )

    def __repr__(self):
        return f'Nave {self.name}'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'crew': self.crew
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="favorite_characters"
    )

    character: Mapped["Character"] = relationship(
        back_populates="favorited_by"
    )

    def __repr__(self):
        return f'A {self.user} le gusta {self.character}'


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )

    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="favorite_planets"
    )

    planet: Mapped["Planet"] = relationship(
        back_populates="favorited_by"
    )

class FavoriteStarship(db.Model):
    __tablename__ = "favorite_starship"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )

    starship_id: Mapped[int] = mapped_column(
        ForeignKey("starship.id"), nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="favorite_starships"
    )

    starship: Mapped["Starship"] = relationship(
        back_populates="favorited_by"
    )
