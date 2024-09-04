from django.db import models
from django.utils import timezone

class Improvement(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    increase_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Процент увеличения

    def __str__(self):
        return self.name

class User(models.Model):
    user_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    last_collected = models.DateTimeField(null=True, blank=True)

    ref_id = models.BigIntegerField(blank=True, null=True)
    character_id = models.BigIntegerField(default=0)

    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ton_wallet = models.CharField(max_length=255, blank=True, null=True)
    daily_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"

    def collect_all_points(self) -> int:
        """
        Собирает все очки, заработанные пользователем от его персонажей.
        Возвращает общее количество собранных очков.
        """
        total_points = sum(character.collect_points() for character in self.characters.all())
        self.points += total_points
        self.last_collected = timezone.now()  # Обновляем время последнего сбора очков
        self.save()
        return total_points

    def can_buy_character(self, character) -> bool:
        return self.points >= character.cost and character.id == self.character_id + 1

    def buy_character(self, character) -> bool:
        if self.can_buy_character(character):
            self.points -= character.cost
            self.character_id = character.id
            self.save()
            return True
        return False

class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    points_per_hour = models.IntegerField()
    last_collected = models.DateTimeField(default=timezone.now)

    improvements = models.ManyToManyField('Improvement', blank=True)
    last_progress_update = models.DateTimeField(default=timezone.now)

    def calculate_points_per_hour(self) -> int:
        base_points = self.points_per_hour
        total_points = base_points
        for improvement in self.improvements.all():
            total_points += base_points * (improvement.increase_percentage / 100)
        return int(total_points)

    def collect_points(self) -> int:
        now = timezone.now()
        hours_elapsed = (now - self.last_collected).total_seconds() // 3600
        points = int(hours_elapsed * self.points_per_hour)
        if hours_elapsed > 8:
            points = self.points_per_hour * 8
        self.last_collected = now
        self.save()
        return points

class Task(models.Model):
    """
    Модель задания, которое может выполнять пользователь.
    """
    title: str = models.CharField(max_length=200)
    description: str = models.TextField()
    icon: str = models.ImageField(upload_to='icons/')  # Значок задания
    image: str = models.ImageField(upload_to='images/')  # Дополнительное изображение задания
    reward: int = models.PositiveIntegerField()  # Вознаграждение за выполнение задания
    start_date: timezone = models.DateTimeField()
    end_date: timezone = models.DateTimeField()
    is_active: bool = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Wallet(models.Model):
    """
    Модель для хранения данных о привязанном TON-кошельке.
    """
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    wallet_address: str = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.wallet_address}"
