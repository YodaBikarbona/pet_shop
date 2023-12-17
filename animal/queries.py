from animal.models import Animal


def get_animal_by_id(_id: int) -> Animal | None:
    return Animal.objects.filter(id=_id).first()


def get_all_animals() -> list[Animal] | None:
    return Animal.objects.all()


def get_animal_by_animal_id(_animal_id: int) -> Animal | None:
    return Animal.objects.filter(animal_id=_animal_id).first()
