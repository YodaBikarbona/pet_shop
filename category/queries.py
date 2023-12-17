from category.models import Category


def get_category_by_name(_name: str) -> Category | None:
    return Category.objects.filter(name=_name).first()


def get_category_by_id(_id: int) -> Category | None:
    return Category.objects.filter(id=_id).first()


def get_all_categories() -> list[Category] | None:
    return Category.objects.all()
