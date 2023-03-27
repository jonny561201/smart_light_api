from sqlalchemy import orm, create_engine
from svc.constants.settings_state import Settings
from svc.db.models.user_information_model import UserCredentials
from werkzeug.exceptions import Unauthorized


class UserDatabaseManager:
    db_session = None

    def __enter__(self):
        settings = Settings.get_instance()
        connection = f'postgresql://{settings.db_user}:{settings.db_pass}@localhost:{settings.db_port}/{settings.db_name}'

        db_engine = create_engine(connection)
        session = orm.sessionmaker(bind=db_engine)
        self.db_session = orm.scoped_session(session)

        return UserDatabase(self.db_session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.commit()
        self.db_session.remove()


class LightDatabase:
    def __init__(self, session):
        self.session = session

    def get_user_info(self, user_id):
        user = self.session.query(UserCredentials).filter_by(user_id=user_id).first()
        if user is None:
            raise Unauthorized
        return {'user_id': user.user_id,
                'roles': [self.__create_role(role.role_devices, role.role.role_name) for role in user.user_roles],
                'first_name': user.user.first_name,
                'last_name': user.user.last_name}
