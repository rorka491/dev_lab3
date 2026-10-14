

class BaseService[_Repository]:

    def __init__(self, repo: _Repository) -> None:
        self.repo = repo

