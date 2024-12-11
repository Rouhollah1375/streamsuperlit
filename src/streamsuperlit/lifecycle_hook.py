class OnInit:
    @classmethod
    def handle(cls, obj) -> None:
        if issubclass(obj.__class__, OnInit):
            obj.on_init()

    def on_init(self) -> None:
        pass


class AfterInit:
    @classmethod
    def handle(cls, obj) -> None:
        if issubclass(obj.__class__, AfterInit):
            obj.after_init()

    def after_init(self) -> None:
        pass
