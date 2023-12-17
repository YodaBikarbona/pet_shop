from mark.models import Mark


def get_mark_by_name(_name: str) -> Mark | None:
    return Mark.objects.filter(name=_name).first()


def get_mark_by_id(_id: int) -> Mark | None:
    return Mark.objects.filter(id=_id).first()


def get_all_marks() -> list[Mark] | None:
    return Mark.objects.all()
