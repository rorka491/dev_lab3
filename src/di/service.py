from dishka import Provider, Scope, provide
from src.repositories.sqlalchemy.booking import BookingRepository
from src.repositories.sqlalchemy.transaction import SQLAlchemyTransaction
from src.repositories.sqlalchemy.user import UserRepository
from src.services.auth import AuthService
from src.services.bookings import BookingsService



class ServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self, 
        user_repo: UserRepository,
        sqlalchemy_transaction: SQLAlchemyTransaction
    ) -> AuthService:
        return AuthService(
            user_repo=user_repo,
            sqlalchemy_transaction=sqlalchemy_transaction
        )

    @provide(scope=Scope.REQUEST)
    def booking_service(
        self,
        repo: BookingRepository,
        sqlalchemy_transaction: SQLAlchemyTransaction,
    ) -> BookingsService:
        return BookingsService(repo=repo, sqlalchemy_transaction=sqlalchemy_transaction)